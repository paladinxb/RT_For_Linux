import flet as ft
from test import create_routing_table, network_graph
import pprint
def main(page: ft.Page):
    global network_graph
    page.window_center()
    page.window_maximized = True
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLACK26, use_material3=True)
    page.title = "Router Information"
    page.vertical_alignment = ft.MainAxisAlignment.START
    def add_router(e):
        if not router_name.value:
            router_name.error_text = "Please enter a router name"
            page.update()
        else:
            network_graph[router_name.value] = {"networks": {}}
            router_name.value = ""
            router_name.error_text = None
            page.update()

    def add_network(e):
        # Заполняем network_graph данными
        if not router_name.value or not neighbor_name.value or not last_int.value or not neighbor_ip.value or not prefix.value:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields"))
            page.snack_bar.open = True
            page.update()
        else:
            if router_name.value not in network_graph or not router_name.value.strip():
                page.snack_bar = ft.SnackBar(ft.Text("Router name is empty or not found"))
                page.snack_bar.open = True
                page.update()
            else:
                if neighbor_ip.value not in network_graph[router_name.value]["networks"]:
                    network_graph[router_name.value]["networks"][neighbor_ip.value] = {
                        "last int": last_int.value,
                        "router": neighbor_name.value,
                        "prefix": prefix.value
                    }
                    neighbor_name.value = ""
                    last_int.value = ""
                    neighbor_ip.value = ""
                    prefix.value = ""
                    pprint.pprint(network_graph)
                    page.update()
                    
    def create_routing_table_internal(e):
        start_router = start_router_name.value
        if start_router in network_graph:
            routing_table = create_routing_table(network_graph, start_router)
            
            #routing_table_text.value = str(routing_table)
           # routing_table_text.value = str(routing_table_text)
            routing_table_text.value = routing_table
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Router not found"))
            page.snack_bar.open = True
            page.update()
    routing_table_text = ft.Text("")
    #formatted_data = ft.Text("")
    routing_table_title = ft.Text("Type            Network Number  Admin/Metric    Port Address    Time            Interface")
    router_name = ft.TextField(label="Router name")
    neighbor_name = ft.TextField(label="Neighbor name")
    last_int = ft.TextField(label="Last interface")
    neighbor_ip = ft.TextField(label="Neighbor IP")
    prefix = ft.TextField(label="Prefix")
    start_router_name = ft.TextField(label="Start router name")

    page.add(
        ft.Row([router_name], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton("Add router", on_click=add_router, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([neighbor_name, last_int, neighbor_ip, prefix], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton("Add network", on_click=add_network, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([start_router_name], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton("Create routing table", on_click=create_routing_table_internal, 
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))], 
                                  alignment=ft.MainAxisAlignment.CENTER),                        
        ft.Row([routing_table_title], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([routing_table_text], alignment=ft.MainAxisAlignment.CENTER)

    )

ft.app(target=main)