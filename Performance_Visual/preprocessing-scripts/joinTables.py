import csv, sys

dir = sys.argv[1] + '/'
act_file = sys.argv[2]
user2grade = {}
user2prof = {}
user2act = {}
id2name = {}

# hash_id,id,username
with open(dir+'user_id_map.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    id2name[row[1]] = row[2]

# id,user_id(1),download_url,grade(3),course_id,key,distinction,status(7),verify_uuid,download_uuid,name,created_date,modified_date,error_reason,mode
with open(dir+'certificates.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    user2grade[row[1]] = row[3]

# id,user_id(1),name,language,location,meta,courseware,gender(7),mailing_address,year_of_birth(9),level_of_education(10),goals,allow_certificate(12),country,city
with open(dir+'profiles.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    user2prof[row[1]] = (row[7],row[9],row[10])

num_act = None
activities = None
# username, total, "book", "forum", "page", "poll", "problem", "seq", "video", "wiki"
with open(act_file, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  line = reader.next()
  activities = line[1:]
  num_act = len(activities)
  for row in reader:
    user2act[row[0]] = row[1:]

out = open(dir+"grade.csv", 'w')
out.write("grade,gender,year_of_birth,ed," + ",".join(activities) + "\n")
for user in user2grade:
  if user in user2prof:
    (gender,yob,ed) = user2prof[user]
    if (not (gender == "f")) and (not (gender == "m")):
      gender = "u"
    if ed == "" or ed == "NULL":
      ed = "unknown"

    username = id2name[user]
    act = None
    if username in user2act:
      act = user2act[username]
    else:
      act = ["0" for i in range(num_act)]
    print >>out, "%s,%s,%s,%s,%s" % (user2grade[user],gender,yob,ed,",".join(act))

out.close()
