

def generate_input_files(rows=30, cols=30):

    cellsize = 10
    x0 = 0
    y0 = 0

    x1 = x0 + cols * cellsize
    y1 = y0 + rows * cellsize

    with open('area_extent.csv', 'w') as content:
        content.write(f'{x0},{y0},{x1},{y1},{cols},{rows}')

    agent_id = 0

    with open('location_daisies.csv', 'w') as content:
        for r in range(rows , 0, -1):
            r -= 1
            for c in range(cols):
                x = x0 + c * cellsize + cellsize / 2
                y = y0 + r * cellsize + cellsize / 2
                content.write(f'{x},{y}\n')
                agent_id += 1


if __name__ == '__main__':
    generate_input_files(19, 19)



