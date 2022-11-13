def create_intersect(type, solver):
    if type == 1:
        create_rect(foreground_x, foreground_y, foreground_z, 0.5, 0.1, 0.1)
        create_rect(background_x - 0.1*portion, background_y, background_z, 0.1*portion, 0.5*portion, 0.1*portion)

        if solver == True:
            create_rect(background_x - 0.1*portion, background_y + 0.5, background_z, 0.5*portion, 0.1*portion, 0.1*portion)
            create_rect(background_x + 0.3*portion, background_y, background_z, 0.1*portion, 0.5*portion, 0.1*portion)

    if type == 2:
        create_rect(foreground_x, foreground_y, foreground_z, 0.5, 0.1, 0.1)
        create_rect(background_x - 0.1*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 1.5*portion, 0.1*portion)
        
        if solver == True:
            create_rect(foreground_x + 0.5, foreground_y, foreground_z, 0.1, 0.1, 1)
            create_rect(background_x - 0.1*portion, background_y + 0.75 *portion, background_z, 1*portion, 0.1*portion, 0.1*portion)
            create_rect(background_x + 0.8*portion, background_y , background_z, 0.1*portion, 0.75*portion, 0.1*portion)

    if type == 3:
        create_rect(foreground_x - 0.1, foreground_y, foreground_z, 1, 0.1, 0.1)
        create_rect(background_x - 0.1*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 0.5*portion, 0.1*portion)

        if solver == True:
            create_rect(foreground_x + 0.2, foreground_y, foreground_z, 0.1, 0.1, 0.5 * portion)
            create_rect(background_x , background_y - 0.5 *portion, background_z, 1*portion, 0.1*portion, 0.1*portion)
            create_rect(background_x + 0.7*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 1*portion, 0.1*portion)

    if type == 4:
        create_rect(foreground_x, foreground_y, foreground_z, 0.5, 0.1, 0.1)
        create_rect(background_x - 0.1*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 1*portion, 0.1*portion)
        create_rect(background_x - 0.5*portion, background_y, background_z, 0.5*portion, 0.1*portion, 0.1*portion)
        
        if solver == True:
            create_rect(foreground_x + 0.2, foreground_y, foreground_z, 0.1, 0.1, 0.5 * portion)
            create_rect(background_x , background_y - 0.5 *portion, background_z, 1*portion, 0.1*portion, 0.1*portion)
            create_rect(background_x + 0.5*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 1*portion, 0.1*portion)

    if type == 5:
        create_rect(foreground_x, foreground_y, foreground_z, 0.1, 0.5, 0.1)
        create_rect(background_x - 0.5*portion, background_y+0.3, background_z, 0.5*portion, 0.1*portion, 0.1*portion)

        if solver == True:
            create_rect(foreground_x, foreground_y -0.5, foreground_z, 0.1, 0.5, 0.1)
            create_rect(background_x - 0.5*portion, background_y - 0.1 *portion, background_z, 1*portion, 0.1*portion, 0.1*portion)
            create_rect(background_x - 0.5*portion, background_y - 0.5 *portion, background_z, 0.1*portion, 1*portion, 0.1*portion)

    if type == 6:
        create_rect(foreground_x - 0.5, foreground_y + 0.5, foreground_z, 1, 0.1, 0.1)
        create_rect(background_x , background_y, background_z, 0.1*portion, 0.5*portion, 0.1*portion)

        if solver == True:
            create_rect(foreground_x, foreground_y -0.5, foreground_z, 0.1, 0.5, 0.1)
            create_rect(foreground_x, foreground_y -0.5, foreground_z, 0.5, 0.1, 0.1)
            create_rect(foreground_x + 0.5, foreground_y -0.5, foreground_z, 0.1, 1.5, 0.1)

    if type == 7:
        create_rect(foreground_x+0.1, foreground_y + 0.5, foreground_z, 0.5, 0.1, 0.1)
        create_rect(foreground_x, foreground_y + 0.5, foreground_z-0.5, 0.1, 0.1, 0.5)
        create_rect(background_x , background_y + 0.1*portion, background_z, 0.1*portion, 0.5*portion, 0.1*portion)

        if solver == True:
            create_rect(background_x , background_y + 0.1*portion, background_z - 1*portion, 0.1*portion, 0.1*portion, 1*portion)
            create_rect(foreground_x, foreground_y , foreground_z-0.5, 0.1, 0.5, 0.1)
            create_rect(foreground_x-0.5, foreground_y, foreground_z-0.5, 0.5, 0.1, 0.1)

    if type == 8:
        create_rect(foreground_x, foreground_y + 0.5, foreground_z-0.5, 0.1, 0.1, 0.5)
        create_rect(background_x , background_y, background_z - 0.2*portion, 0.1*portion, 0.5*portion, 0.1*portion)

        if solver == True:
            create_rect(foreground_x, foreground_y , foreground_z-0.5, 0.1, 0.5, 0.1)
            create_rect(foreground_x - 0.5, foreground_y , foreground_z-0.5, 0.5, 0.1, 0.1)
            create_rect(background_x , background_y +0.2, background_z - 1*portion, 0.1*portion, 0.1*portion, 1*portion)

    if type == 9:
        create_rect(foreground_x +0.5, foreground_y, foreground_z-1, 0.1, 0.1, 1)
        create_rect(background_x - 0.5*portion, background_y, background_z - 0.1*portion, 1*portion, 0.1*portion, 0.1*portion)

        if solver == True:
            create_rect(background_x - 0.5*portion, background_y - 1*portion, background_z - 0.1*portion, 0.1*portion, 1*portion, 0.1*portion)
            create_rect(foreground_x , foreground_y, foreground_z-0.5, 1, 0.1, 0.1)
