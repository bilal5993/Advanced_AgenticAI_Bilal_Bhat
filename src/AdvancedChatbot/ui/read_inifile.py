from configparser import ConfigParser

class ReadIni:
    def __init__(self,path="./src/AdvancedChatbot/ui/configuragion.ini"):
        self.config=ConfigParser()
        self.config.read(path)    # here .read(path) loads data from .ini file into the parser which self.config , it does not return anything.

    
    def get_page_title(self):
        return self.config["ChatbotConstants"].get("PAGE_TITLE")
    def get_llm_options(self):
        return self.config["ChatbotConstants"].get("LLM_OPTIONS").split(',')
    def get_usecase_options(self):
        return self.config["ChatbotConstants"].get("USECASE_OPTIONS").split(',')
    def get_groq_moldes(self):
        return self.config["ChatbotConstants"].get("GROQ_MODEL_OPTIONS").split(',')

    

# if __name__=="__main__":
   
#     base_dir = Path(__file__).resolve().parent
#     path = base_dir/"configuragion.ini"
#     obj= ReadIni(path)
#     s= obj.get_groq_moldes()
#     print(s)