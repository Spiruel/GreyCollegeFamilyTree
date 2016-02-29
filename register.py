import smtplib, uuid, csv, time, ast
from itsdangerous import URLSafeTimedSerializer
import string, random
import myfamilytree as ft

def generate_confirmation_token(user):
    serializer = URLSafeTimedSerializer('my_precious')
    return serializer.dumps(user, salt='my_precious_two')

def confirm_token(token, expiration=3600*24):
    serializer = URLSafeTimedSerializer('my_precious')
    try:
        user = serializer.loads(
            token,
            salt='my_precious_two',
            max_age=expiration
        )
    except:
        return False
    return user

def generate_randid(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def send_email(user, familylist, randid, fromaddr = 'noreply@greycollegefamilytree.co.uk'):
    token = str(generate_confirmation_token(user+randid))
    toaddrs = get_email(user)
    
    msg = """from: Grey College Family Tree <spiruel@gmail.com>
to: """+user+""" <"""+toaddrs+""">
content-type: text/html
subject: Grey College Family Tree - Please confirm your college family details

<title>Grey College Family Tree - Confirm your details</title>
<style>
/* -------------------------------------
    GLOBAL
------------------------------------- */
* {
  font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
  font-size: 100%;
  line-height: 1.6em;
  margin: 0;
  padding: 0;
}
img {
  max-width: 600px;
  width: 100%;
}
body {
  -webkit-font-smoothing: antialiased;
  height: 100%;
  -webkit-text-size-adjust: none;
  width: 100% !important;
}
/* -------------------------------------
    ELEMENTS
------------------------------------- */
a {
  color: #348eda;
}
.btn-primary {
  Margin-bottom: 10px;
  width: auto !important;
}
.btn-primary td {
  background-color: #348eda; 
  border-radius: 25px;
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
  font-size: 14px; 
  text-align: center;
  vertical-align: top; 
}
.btn-primary td a {
  background-color: #348eda;
  border: solid 1px #348eda;
  border-radius: 25px;
  border-width: 10px 20px;
  display: inline-block;
  color: #ffffff;
  cursor: pointer;
  font-weight: bold;
  line-height: 2;
  text-decoration: none;
}
.last {
  margin-bottom: 0;
}
.first {
  margin-top: 0;
}
.padding {
  padding: 10px 0;
}
/* -------------------------------------
    BODY
------------------------------------- */
table.body-wrap {
  padding: 20px;
  width: 100%;
}
table.body-wrap .container {
  border: 1px solid #f0f0f0;
}
/* -------------------------------------
    FOOTER
------------------------------------- */
table.footer-wrap {
  clear: both !important;
  width: 100%;  
}
.footer-wrap .container p {
  color: #666666;
  font-size: 12px;
  
}
table.footer-wrap a {
  color: #999999;
}
/* -------------------------------------
    TYPOGRAPHY
------------------------------------- */
h1, 
h2, 
h3 {
  color: #111111;
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
  font-weight: 200;
  line-height: 1.2em;
  margin: 40px 0 10px;
}
h1 {
  font-size: 36px;
}
h2 {
  font-size: 28px;
}
h3 {
  font-size: 22px;
}
p, 
ul, 
ol {
  font-size: 14px;
  font-weight: normal;
  margin-bottom: 10px;
}
ul li, 
ol li {
  margin-left: 5px;
  list-style-position: inside;
}
/* ---------------------------------------------------
    RESPONSIVENESS
------------------------------------------------------ */
/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
.container {
  clear: both !important;
  display: block !important;
  Margin: 0 auto !important;
  max-width: 600px !important;
}
/* Set the padding on the td rather than the div for Outlook compatibility */
.body-wrap .container {
  padding: 20px;
}
/* This should also be a block element, so that it will fill 100% of the .container */
.content {
  display: block;
  margin: 0 auto;
  max-width: 600px;
}
/* Let's make sure tables in the content area are 100% wide */
.content table {
  width: 100%;
}
</style>
</head>

<body bgcolor="#f6f6f6">

<!-- body -->
<table class="body-wrap" bgcolor="#f6f6f6">
  <tr>
    <td></td>
    <td class="container" bgcolor="#FFFFFF">

      <!-- content -->
      <div class="content">
      <table>
        <tr>
          <td>
            <p>Hi there,</p>
            <p>You\'re receiving this email because someone has registered family details as part of the Grey College family tree.</p>
            <p>The college family details are:</p>
            <b>
            <p>College Father: """+get_name(familylist[0])+"""</p>
            <p>College Mother: """+get_name(familylist[1])+"""</p>
            <p>College Child #1: """+get_name(familylist[2])+"""</p>
            <p>College Child #2: """+get_name(familylist[3])+"""</p>
            </b>
            <p>Does this look correct? Click the button below to confirm your place on the family tree.</p>
	    <p><b>You have a time limit of 24 hours before the verification links expire.</b></p>
            <p>Please make sure your family receive their registration email before the expiration time is up. Remember to double check spam/clutter folders.</p>
            <!-- button -->
            <table class="btn-primary" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td>
                  <a href="http://greycollegefamilytree.co.uk/confirm/?token="""+token+"""">--> These details are correct and I wish to be featured on the family tree <--</a>
                </td>
              </tr>
            </table>
            <!-- /button -->
            <p><a href="http://www.greycollegefamilytree.co.uk/register.html">Register more family details here.</a></p>
            <p>Thanks!</p>
            <p><a href="http://www.greycollegefamilytree.co.uk">www.greycollegefamilytree.co.uk</a></p>
          </td>
        </tr>
      </table>
      </div>
      <!-- /content -->
      
    </td>
    <td></td>
  </tr>
</table>
<!-- /body -->

<!-- footer -->
<table class="footer-wrap">
  <tr>
    <td></td>
    <td class="container">
      
      <!-- content -->
      <div class="content">
        <table>
          <tr>
            <td align="center">
              <p>Received this email in error? <a href="mailto:s.j.bancroft@dur.ac.uk?subject=I received an email in error!"><unsubscribe>Please let me know</unsubscribe></a>.
              </p>
            </td>
          </tr>
        </table>
      </div>
      <!-- /content -->
      
    </td>
    <td></td>
  </tr>
</table>
<!-- /footer -->

</body>
"""

    username = 'greycollegefamilytree@gmail.com'
    password = 'eddingtongingercake16'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    print 'Sent mail from' + fromaddr + ' to ' + toaddrs
    server.quit()

def get_name(username):
    with open('greystudents.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            if row[8] == username:
                return row[1] + ' ' + row[0]
        else:
            return username
                
def get_email(username):
    with open('greystudents.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            if row[8] == username:
                return row[9]
        else:
	    return None

def already_registered(familylist):
    with open('families.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            if row[0] in familylist[0:1] or row[1] in familylist[0:1] or row[2] in familylist[2:] or row[3] in familylist[2:]:
                    return True
        else:
            return False
            
def verify_family(family):
    family_details = [ast.literal_eval(str(i)).keys()[0] for i in family]
    if not already_registered(family_details):
        with open('families.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|')
            writer.writerow(family_details)
        ft.readdata()
        return 'Congratulations! Your family should now be fully registered on the family tree. Please allow a short while for your family to appear on the webpage.'
    else:
        return 'Your family is already registered in the family tree!'
    
def confirm_registration(user, rand):
    with open('registrations.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row_num, row in enumerate(reader):
            if str(row[0]) == str(rand):
                for i, person in enumerate(row[1:]):
                    newrow = row
                    if user in ast.literal_eval(person).keys()[0]:
                        if not ast.literal_eval(row[1+i])[user]:
                            with open('registrations.csv', 'rb') as b:
                                rows = csv.reader(b)
                                row_list = []
                                row_list.extend(rows)

                            newrow[1+i] = {user:True}
			    line_to_override = {row_num:newrow}

                            with open('registrations.csv', 'wb') as b:
                                writer = csv.writer(b)
                                for line, row in enumerate(row_list):
                                    data = line_to_override.get(line, row)
                                    writer.writerow(data)

                        for i in newrow[1:]:
                            if ast.literal_eval(str(i)).values()[0] != True:
                                break
                        else:
                            print 'All family members verified!!!'
                            return verify_family(newrow[1:])
                        return 'You have successfully registered your place in the family tree. You need to make sure other members of your family also verify before the verification time runs out!'
    return 'Error: Something went wrong when trying to confirm your registration.'
            
def process(familylist):
    for i in familylist:
	if get_email(i) is None:
	    return 'One or more of the usernames are invalid/cannot be found.'
    if not any(familylist.count(x) > 1 for x in familylist): #CHANGE THIS TO NOT
        if not already_registered(familylist):
            with open('registrations.csv', 'a') as write_file:
                writer = csv.writer(write_file, delimiter=',', quotechar='|')
		randid = str(generate_randid(4, "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"))
                family = [randid]
                for i in familylist:
                    family.append({i:False})
                writer.writerow(family)
            for person in familylist:
                print 'Sending verification link to', person
                send_email(person,familylist,randid)
            return 'Success: Received family registration request. Please check your @durham.ac.uk email inbox and spam folder!'
        else:
            return 'Error: Already registered in the family tree database.'
    else:
        return 'Error: Rejected because of duplicates in registration.'
