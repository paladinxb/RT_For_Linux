import heapq

# Создаем пустой словарь network_graph, который будет заполняться вами
network_graph = {}
# Добавляем роутер, его сети и связанные данные в network_graph

# Обновленная функция find_shortest_path
def find_network_by_router(graph, target_router):
    for key, value in graph.items():
        networks = value.get('networks', {})
        for network, info in networks.items():
            if info.get('router') == target_router:
                return network
    return None

def find_shortest_path(graph, start, end):
    min_dist = {router: float('inf') for router in graph}
    min_dist[start] = 0
    previous_router = {}

    priority_queue = [(0, start)]

    while priority_queue:
        current_metric, current_router = heapq.heappop(priority_queue)

        if current_metric > min_dist[current_router]:
            continue

        for network, route_info in graph[current_router]['networks'].items():
            neighbor_router = route_info['router']
            neighbor_metric = route_info.get('metric', 1)  # Используйте метрику, если она доступна, иначе 1
            metric_through_current = current_metric + neighbor_metric
            if metric_through_current < min_dist[neighbor_router]:
                min_dist[neighbor_router] = metric_through_current
                previous_router[neighbor_router] = current_router
                heapq.heappush(priority_queue, (metric_through_current, neighbor_router))

    path = []
    current_router = end
    while current_router:
        path.insert(0, current_router)
        current_router = previous_router.get(current_router)

    if not path or path[0] != start:
        return "Нет пути до целевой сети.", float('inf')

    return path, min_dist[end]

# Обновленная функция create_routing_table
def create_routing_table(graph, start_router):
    table = []  # Список для хранения строк таблицы
    printed_networks = set()  # Множество для отслеживания уже выведенных сетей

    if start_router not in graph:
        print(f"Ошибка: Нет информации о маршрутизаторе {start_router}.")
        return []

    min_dist_graph = {}  # Создаем пустой словарь для хранения минимальных расстояний

    for destination, data in graph.items():
        for network_ip, metrics in data['networks'].items():
            path, min_dist = find_shortest_path(graph, start_router, destination)
            min_dist_graph[network_ip] = min_dist  # Сохраняем минимальное расстояние для каждой сети

    print(f"Таблица маршрутизации для маршрутизатора {start_router}:\n")
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Тип", "Номер сети", "Admin/Metric", "Адрес порта", "Время", "Интерфейс"))
    for destination, data in graph.items():
        for network_ip, metrics in data['networks'].items():
            if len(path) == 2 or len(path) == 1:
                next_net = path[0]
            else:
                next_net = path[1]
            target_router = next_net
            network = find_network_by_router(network_graph, next_net)
            if network_ip in printed_networks:
                continue  # Пропускаем вывод, если сеть уже была выведена
            printed_networks.add(network_ip)

            next_hop = min_dist_graph.get(network_ip, "N/A")
            admin_distance = 120

            if next_hop != "N/A":
                metric = find_shortest_path(network_graph, start_router, destination)  # Извлечь метрику из кортежа
                metric_value = metric[1]
                if metric_value >= 2:
                    metric_value -= 1   # Установка метрики в 0, если исходная метрика равна 1
                elif metric_value==0:
                    metric_value = metric_value
                 # Уменьшение метрики на 1, если исходная метрика больше 1"""
                connection_type = "C" if metric_value ==0 else "R"
                last_int = metrics['last int']
                if connection_type == "C":
                    extra_info = "is directly connected"
                    via = ""
                    time = ""
                else:
                    extra_info = f"{admin_distance}/{metric_value}"
                    via = network[:-1] + "2"
                    time = "00:01:00"
            else:
                metric = float('inf')  # Установка метрики на недостижимое значение
                connection_type = "R"
                last_int = 'N/A'
                extra_info = f"{admin_distance}/{metric_value}"
                via = network[:-1] + "2"
                time = "00:01:00"

            formatted_row = f"{connection_type:<15} {network_ip:<15} {extra_info:<15} {via:<15} {time:<15} {last_int:<15}"
            table.append(formatted_row)
            print(formatted_row)
            

    formatted_table = "\n".join(table)  # Объединяем элементы списка в одну строку с помощью перевода строки
    return formatted_table


