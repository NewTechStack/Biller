from tqdm import tqdm
from rethinkdb import RethinkDB
r = RethinkDB()

r.connect( "146.59.155.94", 28015).repl()

time = r.db("ged").table("timesheet")
filters = [['client'], ['user'], ['client_folder'], ['user', 'client_folder'], ['user', 'client']]

timesheets = list(time.order_by('date').pluck("id").run())
for i in tqdm(range(0, len(timesheets))):
    f = {"following": {"id": {"is_before_id":  None if (i + 1) >= len(timesheets) else timesheets[i + 1]['id'], "is_after_id": timesheets[i - 1]['id'] if i > 0 else None}}}
    time.get(timesheets[i]['id']).update(f).run()

for n in range(len(filters)):
    filter = filters[n]
    tris = time.pluck(filter).distinct().run()
    for tri_i in tqdm(range(len(tris))):
        tri = tris[tri_i]
        timesheets = list(time.filter(tri).order_by('date').pluck("id").run())
        for i in range(len(timesheets)):
            f = {"following": {'/'.join(filter): {"is_before_id": None if (i + 1) >= len(timesheets) else timesheets[i + 1]['id'], "is_after_id": timesheets[i - 1]['id'] if i > 0 else None}}}
            time.get(timesheets[i]['id']).update(f).run()
