def GetUnlocksData():
    cactus = [
        {Items.Pumpkin: 5000},
        {Items.Pumpkin: 20000},
        {Items.Pumpkin: 120000},
        {Items.Pumpkin: 720000},
        {Items.Pumpkin: 4320000},
        {Items.Pumpkin: 25900000}
    ]
    
    carrots = [
        {Items.Wood: 50},
        {Items.Wood: 250},
        {Items.Wood: 1250},
        {Items.Wood: 6250},
        {Items.Wood: 31200},
        {Items.Wood: 156000},
        {Items.Wood: 781000},
        {Items.Wood: 3910000},
        {Items.Wood: 19500000},
        {Items.Wood: 97700000}
    ]
    
    dinosaurs = [
        {Items.Cactus: 2000},
        {Items.Cactus: 12000},
        {Items.Cactus: 72000},
        {Items.Cactus: 432000},
        {Items.Cactus: 2590000},
        {Items.Cactus: 15600000}
    ]
    
    expand = [
        {Items.Hay: 30},
        {Items.Wood: 20},
        {Items.Wood: 30, Items.Carrot: 20},
        {Items.Wood: 100, Items.Carrot: 50},
        {Items.Pumpkin: 1000},
        {Items.Pumpkin: 8000},
        {Items.Pumpkin: 64000},
        {Items.Pumpkin: 512000},
        {Items.Pumpkin: 4100000}
    ]
    
    fertilizer = [
        {Items.Wood: 500},
        {Items.Wood: 1500},
        {Items.Wood: 9000},
        {Items.Wood: 54000}
    ]
    
    grass = [
        {Items.Hay: 100},
        {Items.Hay: 300},
        {Items.Wood: 500},
        {Items.Wood: 2500},
        {Items.Wood: 12500},
        {Items.Wood: 62500},
        {Items.Wood: 312000},
        {Items.Wood: 1560000},
        {Items.Wood: 7810000},
        {Items.Wood: 39100000}
    ]
    
    leaderboard = [{
        Items.Bone: 2000000,
        Items.Gold: 1000000
    }]
    
    mazes = [
        {Items.Weird_Substance: 1000},
        {Items.Cactus: 12000},
        {Items.Cactus: 72000},
        {Items.Cactus: 432000},
        {Items.Cactus: 2590000},
        {Items.Cactus: 15600000}
    ]
    
    megafarm = [
        {Items.Gold: 2000},
        {Items.Gold: 8000},
        {Items.Gold: 32000},
        {Items.Gold: 128000},
        {Items.Gold: 512000}
    ]
    
    operators = [{
        Items.Hay: 150,
        Items.Wood: 10
    }]
    
    plant = [{Items.Hay: 50}]
    
    polyculture = [
        {Items.Pumpkin: 3000},
        {Items.Bone: 10000},
        {Items.Bone: 50000},
        {Items.Bone: 250000},
        {Items.Bone: 1250000}
    ]
    
    pumpkins = [
        {Items.Wood: 500, Items.Carrot: 200},
        {Items.Carrot: 1000},
        {Items.Carrot: 4000},
        {Items.Carrot: 16000},
        {Items.Carrot: 64000},
        {Items.Carrot: 256000},
        {Items.Carrot: 1020000},
        {Items.Carrot: 4100000},
        {Items.Carrot: 16400000},
        {Items.Carrot: 65500000}
    ]
    
    speed = [
        {Items.Hay: 20},
        {Items.Wood: 20},
        {Items.Wood: 50, Items.Carrot: 50},
        {Items.Carrot: 500},
        {Items.Carrot: 1000}
    ]
    
    sunflowers = [{Items.Carrot: 500}]
    
    trees = [
        {Items.Wood: 50, Items.Carrot: 70},
        {Items.Hay: 300},
        {Items.Hay: 1200},
        {Items.Hay: 4800},
        {Items.Hay: 19200},
        {Items.Hay: 76800},
        {Items.Hay: 307000},
        {Items.Hay: 1230000},
        {Items.Hay: 4920000},
        {Items.Hay: 19700000}
    ]
    
    watering = [
        {Items.Wood: 50},
        {Items.Wood: 200},
        {Items.Wood: 800},
        {Items.Wood: 3200},
        {Items.Wood: 12800},
        {Items.Wood: 51200},
        {Items.Wood: 205000},
        {Items.Wood: 819000},
        {Items.Wood: 3280000}
    ]
    data = {
        Unlocks.Cactus: cactus,
        Unlocks.Carrots: carrots,
        Unlocks.Dinosaurs: dinosaurs,
        Unlocks.Expand: expand,
        Unlocks.Fertilizer: fertilizer,
        Unlocks.Grass: grass,
        Unlocks.Leaderboard: leaderboard,
        Unlocks.Mazes: mazes,
        Unlocks.Megafarm: megafarm,
        Unlocks.Operators: operators,
        Unlocks.Plant: plant,
        Unlocks.Polyculture: polyculture,
        Unlocks.Pumpkins: pumpkins,
        Unlocks.Speed: speed,
        Unlocks.Sunflowers: sunflowers,
        Unlocks.Trees: trees,
        Unlocks.Watering: watering
    }
    
    return data
    
data = GetUnlocksData()
unlock_list = []

for u in data:
    l = data[u]
    
    for index in range(len(l)):
        items_dict = l[index]
        unlock_info = {Unlocks:u, "KEY_ORDER":index}
        total = 0    
        for item in (Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin, Items.Cactus, Items.Gold, Items.Bone, Items.Weird_Substance):
            amount = 0
            if item in items_dict:
                amount = items_dict[item]
            total += amount
            
            unlock_info[item] = amount
            
        unlock_info[Items] = total
        unlock_list.append(unlock_info)
        
quick_print(unlock_list)
