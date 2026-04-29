from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import cv2

from controller_bridge.serial_controller import RobotController, RobotControllerError
from robot_core.robot import SegmentPolkanRobot
from robot_core.scenario import RobotScenario, Point3D
from robot_core.telemetry import build_telemetry
from analyzer_sip.sip_client import SIPAnalyzer

app = FastAPI(title="Segment-Polkan Operator UI")
templates = Jinja2Templates(directory="operator_ui/templates")

# Для отладки без железа mock=True. На Raspberry Pi с подключенным контроллером поставить mock=False.
controller = RobotController(mock=True)
robot = SegmentPolkanRobot(controller)
analyzer = SIPAnalyzer(mock=True)
scenario = RobotScenario(robot, analyzer)

camera_index = 0


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/ping")
def ping():
    return {"response": controller.ping()}


@app.post("/api/enable")
def enable():
    return {"response": robot.enable()}


@app.post("/api/disable")
def disable():
    return {"response": robot.disable()}


@app.post("/api/stop")
def stop():
    try:
        return {"response": robot.stop()}
    except RobotControllerError as exc:
        return {"error": str(exc)}


@app.post("/api/home")
def home():
    return {"response": robot.home()}


@app.post("/api/move_joint")
def move_joint(joint: int, angle: float, speed_us: int = 700):
    return {"response": robot.move_joint(joint, angle, speed_us)}


@app.post("/api/move_xyz")
def move_xyz(x: float, y: float, z: float, pitch: float = 0.0, speed_us: int = 700):
    return {"response": robot.move_to_xyz(x, y, z, pitch, speed_us)}


@app.post("/api/tongue_touch")
def tongue_touch():
    return {"response": robot.tongue_touch()}


@app.post("/api/tongue_release")
def tongue_release():
    return {"response": robot.tongue_release()}


@app.get("/api/status")
def status():
    try:
        controller_status = robot.status()
        err = None
    except Exception as exc:
        controller_status = controller.last_status
        err = str(exc)
    return build_telemetry(controller_status, analyzer.status, video_enabled=True, last_error=err).to_dict()


@app.post("/api/scenario_collect")
def scenario_collect(sample_x: float, sample_y: float, sample_z: float, analyzer_x: float, analyzer_y: float, analyzer_z: float):
    result = scenario.collect_and_analyze(
        Point3D(sample_x, sample_y, sample_z),
        Point3D(analyzer_x, analyzer_y, analyzer_z),
    )
    return result


def mjpeg_frames():
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        # Пустой генератор, если камеры нет.
        return
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        ok, encoded = cv2.imencode('.jpg', frame)
        if not ok:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded.tobytes() + b'\r\n')


@app.get("/video")
def video():
    return StreamingResponse(mjpeg_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
