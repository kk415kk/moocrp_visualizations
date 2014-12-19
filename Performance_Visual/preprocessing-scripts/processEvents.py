import csv, sys

filename = sys.argv[1]

activities = ["book", "forum", "page", "poll", "problem", "seq", "video", "wiki"]
act2index = {}
index = 1
for act in activities:
  act2index[act] = index
  index += 1

user2act = {}
user2event = {}

# time,secs_to_next,actor(2),verb(3),object_name(4),object_type,result,meta,ip,event(9),event_type(10),page,agent
with open(filename, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    user = row[2]
    verb = row[3]
    if not (user in user2act):
      user2act[user] = [0 for i in range(index)]
      user2event[user] = None

    last = user2event[user]
    if last and row[3] == last[3] and row[4] == last[4] and row[9] == last[9] and row[10] == last[10]:
      continue
      
    entry = user2act[user]
    entry[0] += 1
    for act in activities:
      if verb.find(act) >= 0:
        entry[act2index[act]] += 1
        break
    user2event[user] = row

out = open(filename[:-4]+"_activities_nodup.csv",'w')
out.write("actor,total,")
out.write(",".join(activities) + "\n")
for user in user2act:
  out.write(user)
  entry = user2act[user]
  for e in entry:
    out.write(","+str(e))
  out.write("\n")
out.close()
