import json

class EasyCode():
	def __init__(self):
		self.JsonParsed = None
		self.Includes = ""
		self.Code = ""
		self.Public = ""
		self.Private = ""

	def ParseFromFile(self, file):
		f = open(file)
		self.JsonParsed = json.loads(f.read())

	def GenCppCode(self):
		kMapHdr = "\n#include <map>"
		kVectorHdr = "\n#include <vector>"
		kStringHdr = "\n#include <string>"
		for Class in self.JsonParsed:
			self.Public = ""
			self.Private = ""
			for ClassMember in self.JsonParsed[Class]:
				if "string" in ClassMember["type"] and kStringHdr not in self.Includes:
					self.Includes += kStringHdr
				if "vector" in ClassMember["type"] and kVectorHdr not in self.Includes:
					self.Includes += kVectorHdr
				if "map" in ClassMember["type"] and kMapHdr not in self.Includes:
					self.Includes += kMapHdr

				MemberType = ClassMember["type"]
				if "string" in MemberType:
					if "std::string" not in MemberType:
						MemberType = MemberType.replace("string", "std::string")
				if "vector" in MemberType:
					if "std::vector" not in MemberType:
						MemberType = MemberType.replace("vector", "std::vector")
				if "map" in MemberType:
					if "std::map" not in MemberType:
						MemberType = MemberType.replace("map", "std::map")

				self.Private += "\n\t" + MemberType + " " + ClassMember["name"] + "_;"
				self.Public += "\n\t" + MemberType + " " + ClassMember["name"]
				self.Public += "() { return " + ClassMember["name"] + "_; }"
				self.Public += "\n\t" + "void set_" + ClassMember["name"] + "("
				self.Public += MemberType + " " + ClassMember["name"] + ") { "
				self.Public += ClassMember["name"] + "_" + " = " + ClassMember["name"] + "; }"

				if MemberType == "std::string" :
					self.Public += "\n\t" + "void set_" + ClassMember["name"] + "(char *"
					self.Public +=  ClassMember["name"] + ") { " + ClassMember["name"]
					self.Public += "_" + " = " + ClassMember["name"] + "; }"
					self.Public += "\n\t" + "void set_" + ClassMember["name"] + "(const char *"
					self.Public +=  ClassMember["name"] + ") { " + ClassMember["name"]
					self.Public += "_" + " = " + ClassMember["name"] + "; }"

			self.Code += "\n\nclass " + Class
			self.Code += " {\n public:" + self.Public + "\n private:" + self.Private + "\n};"

		self.Code = self.Includes + self.Code

	def WriteToFile(self, file):
		with open(file, "w") as f:
			f.write(self.Code)
			f.close()

if __name__ == '__main__':
	test = EasyCode()
	test.ParseFromFile("./test.json")
	test.GenCppCode()
	test.WriteToFile("./test.cc")