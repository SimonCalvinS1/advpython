class ChristUni:
    uni = "Christ University"
    courses = ["BBA", "BCom", "BA", "BCA", "BEd", "BE", "BTech", "BSc", "BBA-LLB", "BA-LLB", "BCom-LLB"]
    def printUni(self):
        print(f"University: {self.uni}")
    def printCourses(self):
        print("Available courses:")
        for course in self.courses:
            print(f" - {course}")
    def welcome(self, name):
        cap_name = name.upper()
        print(f"Welcome to {self.uni}, {cap_name}")

class SchoolofSciences:
    school = "School of Sciences"
    depts = ["Computer Science", "Mathematics", "Life Sciences", "Statistics and Data Science", "Electronics", "Physics", "Chemistry"]
    def printSci(self, name):
        cap_name = name.upper()
        print(f"Welcome to {self.school}, {cap_name}")
    def printDepts(self):
        for dept in self.depts:
            print(f" - {dept}")

class DeptCompSci:
    programmmes = ["BCA", "BSc CM", "BSc CS", "MSc AI/ML", "MSc Data Science", "MCA", "PHD in Computer Science"]
    def printCompSci(self, name):
        cap_name = name.upper()
        print(f"Welcome to the Department of Computer Science, {cap_name}")
    def printProg(self):
        print("Computer Science Programmes:")
        for prog in self.programmmes:
            print(f" - {prog}")

christ_obj = ChristUni()
christ_obj.printUni()
christ_obj.printCourses()
christ_obj.welcome("Simon")

sci_obj = SchoolofSciences()
sci_obj.printSci("Calvin")
sci_obj.printDepts()

comp_sci_obj = DeptCompSci()
comp_sci_obj.printCompSci("Bob")
comp_sci_obj.printProg()