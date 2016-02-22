import simplejson as json
from itertools import count
import os,time
import csv

'''
INCOMPATIBILITIES:
lack of spouse but do have children
remarriages
more than two children
children with a year gap of more than 1 from their parents
'''

empty_node_id = 1
marriages = []
people = []
people_used = []

class Marriage:
    def __init__(self, year, husband, wife, children):
            self.year = 0
            self.husband = husband
            self.wife = wife 
            self.children = children
            
    def get_year(self):
        return self.marriageYear 
        
    def set_year(self, year):
        self.marriageYear = year

    def add_child(self, child):
        self.children.append(child)  
        
    def get_members(self):
        return [self.husband, self.wife]  

    def is_member(self, person):
        return person in self.get_members()          
        
    def get_children(self):
        return self.children
        
    def __str__(self):
        return "Year: " + str(self.year) + ", Husband: " + self.husband.get_name() + ", Wife: " + self.wife.get_name()

class Person:
    id_counter = count()
    def __init__(self, username, forename='', surname='', subject='unknown', year='unknown'):
            self.username = username
            self.forename = forename.title()
            self.surname = surname.title()
            if self.surname[0:2].lower() == 'mc':
                self.surname = self.surname[0].upper() + self.surname[1:2] + self.surname[2].upper() + self.surname[3:]
            self.subject = subject.replace('\"','')
            self.id = next(self.id_counter)+1
            
    def get_username(self):
        return self.username
        
    def get_name(self):
        if self.forename is '' and self.surname is '':
            return self.username.title()
        else:
            return self.forename + ' ' + self.surname
    
    def get_subject(self):
        return self.subject
    
    def get_year(self):
        return self.year
         
    def get_id(self):
        return self.id
        
    def get_parents(self):
        for x in marriages:
            if self in x.get_children():
                return [x.husband, x.wife]
        else:
            return ['None','None']
        
    def get_parents_id(self):
        for x in marriages:
            if self in x.get_children():
                return [x.husband.get_id(), x.wife.get_id()]
            else:
                return ['None','None']
        
    def get_other_partner(self):
        marriage = get_marriage(self)
        if marriage is None:
            return 'None'
        else:
            if self == marriage.husband:
                return marriage.wife
            else:
                return marriage.husband

    def get_gender(self):
        marriage = get_marriage(self)
        if marriage is None:
            return 'M'
        else:
            if self == marriage.husband:
                return 'M'
            else:
                return 'F'
        
def get_user_details(username):
    with open('/var/www/greycollegefamilytree.co.uk/http/familytree/greystudents.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if username == str(row[8])[1:-1]:
                details = username, row[1].split(' ')[0].replace('"',''), row[0].replace('"',''), row[6]
                return details
        else:
            return username.upper()
            
def empty_node():
    global empty_node_id
    empty_node_id = empty_node_id + 1
    return str(empty_node_id)

def exists_already(familymember):
    if get_person(familymember) == []:
        userdetails = get_user_details(familymember)
        if type(userdetails) is not tuple:
            return list_append(people, Person(userdetails))
        else:
            return list_append(people, Person(userdetails[0], userdetails[1], userdetails[2], userdetails[3]))
    else:
        return get_person(familymember)[0]
            
def readdata():
    parents1, parents2, children1, children2 = [],[],[],[]
    with open('/var/www/greycollegefamilytree.co.uk/http/familytree/families.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_ALL)
        for row in reader:
                parent1 = str(row[0])
                parent2 = str(row[1])
                child1 = str(row[2])
                child2 = str(row[3])
                parents1.append(parent1)
                parents2.append(parent2)
                children1.append(child1)
                children2.append(child2)
    for i in range(len(parents1)):
        parents1_nospace = exists_already(parents1[i])
        parents2_nospace = exists_already(parents2[i])
        children1_nospace = exists_already(children1[i])
        children2_nospace = exists_already(children2[i])
        marriages.append(Marriage(2014, parents1_nospace, parents2_nospace, [children1_nospace, children2_nospace]))

def list_append(lst, item):
    lst.append(item)
    return item

def get_mode(array):
    most = max(list(map(array.count, array)))
    if most == 1:
        return ['unknown']
    else:
        return list(set(filter(lambda x: array.count(x) == most, array)))
        
def capitalise_nth(s, n):
    return s[:n].lower() + s[n:].capitalize()
    
def get_marriage(person):
    return next((x for x in marriages if x.is_member(person)), None)
    
def get_root_people():
    marriedPeople = [j for i in [i.get_children() for i in marriages] for j in i]
    return [x for x in people if x not in marriedPeople]
        
def similar_string(w1, w2):
    w1 = w1 + ' '*(len(w2)-len(w1))
    w2 = w2 + ' '*(len(w1)-len(w2))
    return sum([1 if i==j else 0 for i,j in zip(w1,w2)])/float(len(w1))
    
def get_person(name='', id=999999999999):
    for person in people:
        person_name = person.get_name().lower()
        if person.get_username() == name:
            return [person]
        elif person_name == name.lower():
            return [person]
        elif int(person.get_id()) == int(id):
            return [person]
        split_person_name = person_name.split()
        if len(split_person_name[0]) >= 3 and name.lower().split() != []:
            if split_person_name[0][:2] == name.lower().split()[0][:2] and split_person_name[-1] == name.lower().split()[-1]:
                return [person]
    else:
        return []
    
def get_root_partners():
    rootPeople = get_root_people()
    rootPartners = []
    uniqueMarriages = []
    for person in rootPeople:
        marriage = get_marriage(person)
        if marriage == None:
            rootPartners.append(person)
        elif marriage not in uniqueMarriages:
            rootPartners.append(marriage.get_members()[0])
            uniqueMarriages.append(marriage)
    return rootPartners
    
def get_root_marriages():
    rootPeople = get_root_people()
    rootMarriages = [get_marriage(x) for x in rootPeople]
    unique = []
    [unique.append(item) for item in rootMarriages if item not in unique and item != None]
    return unique

def get_family_stats(people_used):
    subjects = [x.get_subject() for x in people_used]
    mode_subjects = get_mode(subjects)
    if len(mode_subjects) > 1 and 'unknown' in mode_subjects:
        mode_subjects.remove('unknown')
    if len(mode_subjects) > 1:
        mode_subjects = 'The most common subjects for this family are ' + ','.join(mode_subjects[:len(mode_subjects)-1]) + ' and ' + mode_subjects[-1]
    if len(mode_subjects) == 1:
        mode_subjects = 'The most common subject for this family is ' + str(mode_subjects[0])
    return '''<p>There are ''' + str(len(people_used)) + ''' known members of this college family.</p>
    <p>'''+str(mode_subjects)+'''.</p>'''
    
def get_start_node(person):
    if person.get_parents() != ['None','None']:
        return get_start_node(person.get_parents()[0])
    elif person.get_other_partner().get_parents() != ['None','None']:
        return get_start_node(person.get_other_partner().get_parents()[0])
    else:
        if person not in rootPeople:
            return get_start_node(person.get_other_partner())
        else:
            return person
        
def make_connections():
    rootPeople = get_root_partners()
    connections = ''
    for x in people_used:
        if [a.get_name() for a in people_used].count(x.get_name()) > 1:
            people_used.remove(x)
    for x in people_used:
        if not (people_used.index(x)+1) % 2:
            continue

        marriage_info = get_marriage(x)
        if marriage_info is not None:
            husband, wife = marriage_info.husband.get_name(), marriage_info.wife.get_name()
            husband_id, wife_id = marriage_info.husband.get_id(), marriage_info.wife.get_id()

            if marriage_info.husband not in people_used or marriage_info.wife not in people_used:
                continue

            source = {'id': husband_id, 'name': str(husband)}
            target = {'id': wife_id, 'name': str(wife)}
            obj = {'source': source, 'target': target}
            if x != rootPeople[-2]:
                connections = connections + str(json.dumps(obj, sort_keys=True, indent=4 * ' ') + ',')
            else:
                connections = connections + str(json.dumps(obj, sort_keys=True, indent=4 * ' ') + ',') #used to be without comma but now it needs this
    return connections

def get_children_nodes(children):
    child_nodes = None
    for child in children:
        current_obj = root_nodes(child)
        if child_nodes is None:
            child_nodes = current_obj
        else: 
            child_nodes = child_nodes, current_obj
    return child_nodes
       
def root_nodes(people, first_node=False):
    obj = None
    if type(people) != list: 
        people = [people]
    for person in people:
        if person in rootPeople and first_node:
            first_node = False
            return {'name': "", 'id': 'year0', 'hidden': 'true', 'children': root_nodes(people)}
        else:
            marriage_info = get_marriage(person)
            if marriage_info is None:
                current_obj = {'name': person.get_name(), 'id': person.get_id(), 'children': []}
                people_used.append(person)
                if obj is None:
                    obj = []
                obj.append(current_obj)
            else:
                partners = marriage_info.get_members()
                husband, wife = partners[0].get_name(), partners[1].get_name()
                husband_id, wife_id = marriage_info.husband.get_id(), marriage_info.wife.get_id()
                marriage_year = marriage_info.year
                children = marriage_info.get_children()
                people_used.append(partners[0])
                people_used.append(partners[1])
                children_tuple = get_children_nodes(children)
                children_list = [element for tupl in children_tuple for element in tupl]
                if partners[0].get_parents() == ['None', 'None'] or partners[1].get_parents() == ['None', 'None']:
                    if partners[0].get_parents() == ['None', 'None'] and partners[1].get_parents() == ['None', 'None']:
                        current_obj = {'name': str(husband), 'id': husband_id, 'no_parent': 'true'}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'no_parent': 'true', 'children': []}               
                    if partners[0].get_parents() == ['None', 'None'] and partners[1].get_parents() != ['None', 'None']:
                        current_obj = {'name': str(husband), 'id': husband_id, 'no_parent': 'true'}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'children': []}
                    if partners[0].get_parents() != ['None', 'None'] and partners[1].get_parents() == ['None', 'None']:
                        current_obj = {'name': str(husband), 'id': husband_id}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'no_parent': 'true', 'children': []}              
                else:
                    if not any((True for person in partners[0].get_parents() if person in people_used)):
                        current_obj = {'name': str(husband), 'id': husband_id, 'no_parent' : 'true'}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'children': []}
                    elif not any((True for person in partners[1].get_parents() if person in people_used)):
                        current_obj = {'name': str(husband), 'id': husband_id}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'no_parent': 'true', 'children': []}
                    else:
                        current_obj = {'name': str(husband), 'id': husband_id}, {'name': '', 'id': 'empty_node_id_' + empty_node(), 'no_parent': 'true', 'hidden': 'true', 'children': children_list}, {'name': str(wife), 'id': wife_id, 'children': []}
                return current_obj
    return obj

def main(start_node=None):
    global rootPeople, obj, people_used
    if start_node is not None: 
        student_name = 'Family Tree for ' + str(start_node.get_name()) + '.'
    else:
        student_name = ''
           
    html_content, root = '', ''
    rootPeople = get_root_partners()

    if start_node is None:
        start_node = rootPeople[0]
    else:
        start_node = get_start_node(start_node)
    
    people_used = []

    root = str(json.dumps(root_nodes(start_node, first_node=True), indent=4 * ' ', sort_keys = True, ensure_ascii=False))
    
    database_stats = 'Family Tree database contains ' + str(len(marriages)) + ' marriages involving ' + str(len(people)) + ' people as of ' + str(time.ctime(os.path.getmtime('/var/www/greycollegefamilytree.co.uk/http/familytree/families.csv'))) + '.'
    family_stats = get_family_stats(people_used)
        
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="">
        <meta name="author" content="">

        <title>Grey College Family Tree</title>
        <script type='text/javascript' src='http://d3js.org/d3.v3.min.js'></script>  

        <!-- Bootstrap Core CSS -->
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">

        <!-- Custom CSS -->
        <link rel="stylesheet" href="/static/css/logo-nav.css">

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
            <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>
         
          <style type='text/css'>
            body {
            font: 10px sans-serif;
        }
        .link {
            fill: none;
            stroke: #000;
        }
        .sibling {
            fill: none;
            stroke: blue;
        }
        .border {
            fill: none;
            shape-rendering: crispEdges;
            stroke: #aaa;
        }
        .node {
            stroke: red;
            fill: white;
        }
          </style>
          
    <script type='text/javascript'>
        window.onload=function(){
        var margin = {
            top: -100,
            right: 10,
            bottom: 50,
            left: 10
        },
        width = 840,
            height = 700;
        var kx = function (d) {
            return d.x - 20;
        };
        var ky = function (d) {
            return d.y - 10;
        };
        //this places the text x axis adjust this to centre align the text
        var tx = function (d) {
            return d.x - 3;
        };
        //this places the text y axis adjust this to centre align the text
        var ty = function (d) {
            return d.y + 3;
        };
        //makes an .SVG
        var svg = d3.select("#graph").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


        //JSON note that 
        //no_parent: true this ensures that the node will not be linked to its parent
        //hidden: true ensures that the nodes is not visible.
        var root = ''' + root + '''
        var allNodes = flatten(root);
        //This maps the siblings together mapping uses the ID using the blue line
        var siblings = [
        '''+make_connections()+'''
        ];

        function wrap(text, width) {
        text.each(function() {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            x = text.attr("x"),
            dy = parseFloat(text.attr("dy")),
            tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").attr("dx", ".5em").text(word);
          }
        }
        });
        }

        // Compute the layout.
        var tree = d3.layout.tree().size([width, height]),
            nodes = tree.nodes(root),
            links = tree.links(nodes);

        // Create the link lines.
        svg.selectAll(".link")
            .data(links)
            .enter().append("path")
            .attr("class", "link")
            .attr("d", elbow);


        var nodes = svg.selectAll(".node")
            .data(nodes)
            .enter();

        //First draw sibling line with blue line
        svg.selectAll(".sibling")
            .data(siblings)
            .enter().append("path")
            .attr("class", "sibling")
            .attr("d", sblingLine);

        // Create the node rectangles.
        nodes.append("a")
            .attr("xlink:href", function(d){return "?id=" + d.id;})  // <-- GET request from id property

        .append("rect")
            .attr("class", "node")
            .attr("height", 30)
            .attr("width", 45)
            .attr("id", function (d) {
            return d.id;
        })
            .attr("display", function (d) {
            if (d.hidden) {
                return "none"
            } else {
                return ""
            };
        })
            .attr("x", kx)
            .attr("y", ky);
        // Create the node text label.
        nodes.append("text")
            .text(function (d) {
            return d.name;
        }).attr("transform", "translate(0," + 5 + ")")
            .style("text-anchor", "middle")
            .attr("x", tx)
            .attr("y", ty)
            .attr("dy", "-0.5em")
            .attr("dx", "0.5em")
            .style("pointer-events", "none")
        .call(wrap, 47.5);


        /**
        This defines the line between spouses.
        **/
        function sblingLine(d, i) {
            //start point
            var start = allNodes.filter(function (v) {
                if (d.source.id == v.id) {
                    return true;
                } else {
                    return false;
                }
            });
            //end point
            var end = allNodes.filter(function (v) {
                if (d.target.id == v.id) {
                    return true;
                } else {
                    return false;
                }
            });
            //define the start coordinate and end co-ordinate
            var linedata = [{
                x: start[0].x,
                y: start[0].y
            }, {
                x: end[0].x,
                y: end[0].y
            }];
            var fun = d3.svg.line().x(function (d) {
                return d.x;
            }).y(function (d) {
                return d.y;
            }).interpolate("linear");
            return fun(linedata);
        }

        /*To make the nodes in flat mode.
        This gets all the nodes in same level*/
        function flatten(root) {
            var n = [],
                i = 0;

            function recurse(node) {
                if (node.children) node.children.forEach(recurse);
                if (!node.id) node.id = ++i;
                n.push(node);
            }
            recurse(root);
            return n;
        }
        /** 
        This draws the lines between nodes.
        **/
        function elbow(d, i) {
            if (d.target.no_parent) {
                return "M0,0L0,0";
            }
            var diff = d.source.y - d.target.y;
            //0.40 defines the point from where you need the line to break out change is as per your choice.
            var ny = d.target.y + diff * 0.40;

            linedata = [{
                x: d.target.x,
                y: d.target.y
            }, {
                x: d.target.x,
                y: ny
            }, {
                x: d.source.x,
                y: d.source.y
            }]

            var fun = d3.svg.line().x(function (d) {
                return d.x;
            }).y(function (d) {
                return d.y;
            }).interpolate("step-after");
            return fun(linedata);
        }
        }//]]>
    </script>

    <body>

        <!-- Navigation -->
        <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
            <div class="container">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="/">
                        <img src="/static/logo.png" alt="" height="65" width="130"> <!--Credit to Teodor Tzokov for the logo-->
                    </a>
                </div>
                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <ul class="nav navbar-nav">
                        <li>
                            <a href="/">Home</a>
                        </li>
                        <li>
                            <a href="/register.html">Register</a>
                        </li>
                    </ul>
                </div>
                <!-- /.navbar-collapse -->
            </div>
            <!-- /.container -->
        </nav>

        <!-- Page Content -->
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    
        
        Search for student name or CIS username:
        <form action="." method="POST">
                <input type="text" name="text">
                <input type="submit" name="my-form" value="Search">
            </form>
        <br>
        
        <h1>'''+str(student_name)+'''</h1>
        <h4>'''+str(family_stats)+'''</h4>
        
        <div id="graph"></div>
        
        <br>
        
        <h4><a href="register.html">Can't find yourself on the family tree? Register your college family here.</a></h4>
        <h3>'''+str(database_stats)+'''</h3>

                </div>
            </div>
        </div>
        <!-- /.container -->
        
        <!-- jQuery -->
        <script src="js/jquery.js"></script>

        <!-- Bootstrap Core JavaScript -->
        <script src="js/bootstrap.min.js"></script>

    </body>

    </html>
    '''
    
    return html_content
    
if __name__ == '__main__':
    readdata()
    main()
