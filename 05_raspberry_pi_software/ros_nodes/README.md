# ROS-слой

Для MVP можно запускать FastAPI напрямую. ROS/ROS2 нужен, когда появятся несколько узлов:
- camera_node;
- arm_control_node;
- telemetry_node;
- analyzer_node;
- operator_bridge_node.

Ниже — минимальная заготовка ROS2-ноды. Для запуска нужен установленный ROS2.
