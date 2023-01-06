def schedule(txs, shared_obj_num):
    wait = []
    for tx in txs:
        s = set()
        l = len(tx)
        for o in tx:
            if o <= shared_obj_num:
                s.add(o)
        wait.append([l, s])

    time = 0
    occupied = set()
    executing = {}

    while wait:
        new_wait = []
        for l, s in wait:
            resource_ready = True
            for o in s:
                if o in occupied:
                    resource_ready = False
                    break
            if resource_ready:
                finish_time = time + l
                if finish_time in executing.keys():
                    executing[finish_time] =  s.union(executing[finish_time])
                else:
                    executing[finish_time] = s
                for o in s:
                    occupied.add(o)
            else:
                new_wait.append([l,s])
        wait = new_wait

        finish_time, freed_res = sorted(executing.items())[0]
        time = finish_time
        executing.pop(finish_time, None)
        for o in freed_res:
            occupied.remove(o)

    return time