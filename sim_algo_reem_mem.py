from collections import deque

def procesar(segmentos, reqs, marcos_libres):
    page_size = 0x10  
    fifo_queue = deque()
    page_table = {}  
    results = []

    for req in reqs:
        # Verificar si la dirección lógica está en algún segmento
        found = False
        for nombre, base, limite in segmentos:
            if base <= req < base + limite:
                found = True
                break

        if not found:
            results.append((req, 0x1FF, "Segmentation Fault"))
            continue

        # Calcular la página y offset
        page_number = req // page_size
        offset = req % page_size

        # Verificar si la página ya está asignada
        if page_number in page_table:
            marco = page_table[page_number]
            direccion_fisica = (marco * page_size) + offset
            results.append((req, direccion_fisica, "Marco ya estaba asignado"))
        else:
            # Asignar marco
            if len(fifo_queue) < len(marcos_libres):
                marco = marcos_libres[len(fifo_queue)]
                fifo_queue.append(page_number)
                page_table[page_number] = marco
                direccion_fisica = (marco * page_size) + offset
                results.append((req, direccion_fisica, "Marco libre asignado"))
            else:
                # Reemplazo FIFO
                old_page = fifo_queue.popleft()
                old_marco = page_table.pop(old_page)
                fifo_queue.append(page_number)
                page_table[page_number] = old_marco
                direccion_fisica = (old_marco * page_size) + offset
                results.append((req, direccion_fisica, "Marco asignado"))

    return results

def print_results(results):
    for req, direccion, accion in results:
        print(f"Req: {req:#04x} Direccion Fisica: {direccion:#04x} Acción: {accion}")

if __name__ == '__main__':
    marcos_libres = [0x0, 0x1, 0x2]
    reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
    segmentos = [
        ('.text', 0x00, 0x1A),
        ('.data', 0x40, 0x28),
        ('.heap', 0x80, 0x1F),
        ('.stack', 0xC0, 0x22),
    ]

    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)