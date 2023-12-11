from newspaper import Config
from newspaper import Article
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' #Change yours
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

def sum_txt(url):
    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = 'cpu'

    #address = 'https://vietcetera.com/vn/tu-khi-nao-lan-da-can-dung-my-pham-cong-nghiep'
    article = Article(url, config=config)
    article.download()
    article.parse()
    # the replace is used to remove newlines
    article_text = article.text.replace('\n', ' ')
    #print(article_text)

    """
    tokenizer = AutoTokenizer.from_pretrained("C:\\Users\\ACER\\AI\\sum_txt\\MLnews\\MLnews\\pythonvit5\\vit5-large-vietnews-summarization")  
    model = AutoModelForSeq2SeqLM.from_pretrained("C:\\Users\\ACER\\AI\\sum_txt\\MLnews\\MLnews\\pythonvit5\\vit5-large-vietnews-summarization")
    # tokenizer = AutoTokenizer.from_pretrained("pythonvit5")  
    # model = AutoModelForSeq2SeqLM.from_pretrained("pythonvit5")
    print("OK")
    model.to(device)

    sentence = article_text
    text =  sentence
    encoding = tokenizer(text, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=256,
        early_stopping=True
    )
    content = ""
    for output in outputs:
        line = tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        #print(line)
        content = content + " " + line
    return content
    """
    API_URL = "https://api-inference.huggingface.co/models/VietAI/vit5-large-vietnews-summarization"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": article_text,
    })

    return output[0]['summary_text']

def getAuthor(url):
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.authors

def getDate(url):
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.publish_date

def getTopimg(url):
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.top_image

def getTopvid(url):
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.movies

def getKeyword(url):
    article = Article(url, config=config)
    article.download()
    article.parse()
    article.nlp()
    return article.keywords
