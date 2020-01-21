import requests 
  
# defining the api-endpoint  
API_ENDPOINT = "https://cdv22626-test10.azurewebsites.net/newevent"
  
# your API key here 
API_KEY = "JebanjeFjelkyKutsz666"
  
# data to be sent to api 
data = {'Token':API_KEY, 
        'api_option':'paste', 
        'EventType':'pajton', 
        'Value':'szatan'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url)