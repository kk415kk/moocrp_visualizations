import csv, sys

def num_intersect(a,b):
  n = 0
  for x in a:
    if x in b:
      n += 1
  return n

def intersect(a,b):
  ans = []
  for x in a:
    if x in b:
      ans.append(x)
  return ans

dir = sys.argv[1] + '/'
act_file = sys.argv[2]

users = []
users_cert = []
cert_groups = {}
users_enroll = []
enroll_groups = {}
users_prof_allow = []

# id,user_id,download_url,grade,course_id,key,distinction,status(7),verify_uuid,download_uuid,name,created_date,modified_date,error_reason,mode
with open(dir+'certificates.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    users_cert.append(row[1])
    st = row[7]
    if st in cert_groups:
      cert_groups[st].append(row[1])
    else:
      cert_groups[st] = [row[1]]

# id,user_id,course_id,created,is_active(4),mode
with open(dir+'enrollment.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    users_enroll.append(row[1])
    st = row[4]
    if st in enroll_groups:
      enroll_groups[st].append(row[1])
    else:
      enroll_groups[st] = [row[1]]

# id,user_id,name,language,location,meta,courseware,gender,mailing_address,year_of_birth,level_of_education,goals,allow_certificate(12),country,city
with open(dir+'profiles.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    if row[12] == "1":
      users_prof_allow.append(row[1])

id2name = {}
name2id = {}
# hash_id,id,username
with open(dir+'user_id_map.csv', 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    users.append(row[1])
    id2name[row[1]] = row[2]
    name2id[row[2]] = row[1]

act_users = []
act_not_in_map = 0
act_not_in_map_list = []
log_not_in_map = 0
# username, total, "book", "forum", "page", "poll", "problem", "seq", "video", "wiki"
with open(act_file, 'rb') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  reader.next()
  for row in reader:
    if row[0] in name2id:
      act_users.append(name2id[row[0]])
    else:
      act_not_in_map += 1
      act_not_in_map_list.append(row[0])
      log_not_in_map += int(row[1])

print "enroll", len(users_enroll)
print "enroll ^ users", num_intersect(users_enroll, users)
print "cert", len(users_cert)
print "cert_yes", len(cert_groups["downloadable"])
print "cert_no", len(cert_groups["notpassing"])
# print "enroll_active", len(enroll_groups['1'])
# print "prof_allow", len(users_prof_allow)
print "cert ^ enroll", num_intersect(users_cert, users_enroll)
print "cert_yes ^ enroll", num_intersect(cert_groups["downloadable"], users_enroll)


# print "cert ^ enroll_active", num_intersect(users_cert, users_enroll_active)
# print "cert_yes ^ enroll_active", num_intersect(cert_groups["downloadable"], users_enroll_active)
# print "cert_no ^ enroll_active", num_intersect(cert_groups["notpassing"], users_enroll_active)

for cert_key in cert_groups:
  for enroll_key in enroll_groups:
    print "cert = %s, enroll_active = %s, N = %d" % (cert_key, enroll_key, num_intersect(cert_groups[cert_key], enroll_groups[enroll_key]))

inactive_cert = intersect(cert_groups["downloadable"], enroll_groups["0"])
print "cert = downloadable, enroll_active = 0, user_id = ", [id2name[x] for x in inactive_cert]


print "----------------------------"
print "act_not_in_map", act_not_in_map
print "log_not_in_map", log_not_in_map
print "act_not_in_map", act_not_in_map_list[:10]
print "act", len(act_users)
print "act ^ enroll", num_intersect(act_users, users_enroll)
print "act ^ cert", num_intersect(act_users, users_cert)
print "cert_yes ^ act", num_intersect(cert_groups["downloadable"], act_users)

print "cert_yes ^ enroll ^ act", num_intersect(intersect(cert_groups["downloadable"],users_enroll),act_users)
