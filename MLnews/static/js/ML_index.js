// let options = document.querySelectorAll(".options div");
// let cup = document.querySelector(".cup");
// let title = document.querySelector(".title");

// function formatOption(option) {
//     return option.toLowerCase().replace(/\s/g, "-");
// }

// options.forEach((option) => {
//     option.addEventListener("click", function() {
//         options.forEach((opt) => {
//             cup.classList.remove(formatOption(opt.textContent));
//         });
//         cup.classList.add(formatOption(this.textContent));
//         title.innerHTML = this.textContent;
//     });
// });

function News(title, description,img, img_cnt, pubdate, guid)
{
  this.title = title;
  this.description = description;
  this.guid = guid;
  this.img = img;
  this.img_content = img_cnt;
  this.pubdate = pubdate;
}

async function make_json(URL)
{
  const datas = await Promise.all(URL.map(url => fetch(url).then((response) => response.text().then((str) => new window.DOMParser().parseFromString(str, 'text/xml')))))
  data_json = [];
  news_json = new Array();
  for (data of datas) {
    
    const items = data.querySelectorAll('item');
    items.forEach((item) => {
      const title = item.getElementsByTagName('title');
      const description = item.getElementsByTagName('description')
      const pubdate = item.getElementsByTagName('pubDate')
      const guid = item.getElementsByTagName('guid');

      for (let i = 0; i < guid.length; i++) {
        let title_txt = title[i].textContent
          .replaceAll('\n', '')
          .replaceAll('\t', '')
          .trim(); 
        
          let description_txt = description[i].textContent
          .replaceAll('\n', '')
          .replaceAll('\t', '')
          .trim(); 
          let img = description_txt.replaceAll(/\s/g,'').substring(description_txt.indexOf("src=")+3).substring(0,description_txt.substring(description_txt.indexOf("src=")+5).indexOf(">")-1);
          if(img.substr(img.length - 1) == '\"')
          {
            img = img.slice(0, -1);
          }
          let img_content = description_txt.substring(description_txt.indexOf("</a>")+4, description_txt.length-1).replace("</br>", "");
          //console.log(img);
        
          let pubDate = pubdate[i].textContent
          .replaceAll('\n', '')
          .replaceAll('\t', '')
          .trim(); 
        
        let guid_txt = guid[i].textContent
          .replaceAll('\n', '')
          .replaceAll('\t', '')
          .trim(); 

            news_json.push(new News(title_txt, description_txt, img, img_content, pubDate, guid_txt));
          for (i = 0; i < news_json.length; i++) {
              var dict = {}
              dict['Title'] = news_json[i].title
              dict['Description'] = news_json[i].description
              dict['Image'] = news_json[i].img
              dict['Image_content'] = news_json[i].img_content
              dict['Publish_Date'] = Date.parse(news_json[i].pubdate, "ddd, dd MMM yyyy HH:mm:ss zzz");
              dict['Guid'] = news_json[i].guid
              data_json[i] = dict
          }
          data_json.sort(function(x, y){
            return - x.Publish_Date + y.Publish_Date;
        })
          //console.log(data_json);
      }
      }
    );
    }
    return data_json;
}

//Get data
function Load_content(URL){
  document.querySelector('.list_news').innerHTML = "";
  make_json(URL).then((data_json) => {
    for(let json_item=0; json_item< data_json.length; json_item++)
    {
      let datetime = new Date(data_json[json_item].Publish_Date);
      console.log(typeof(datetime));
      let dateFormat = datetime.getHours() + ":" + (datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes() + " "+ datetime.getDate() + "/" +datetime.getMonth() + "/" +datetime.getFullYear();
        let html =`
        <div class="row news">
            <div class="col-4 news_assets">
                <div class="col news_img">
                    <a href=${data_json[json_item].Guid}>
                        <img src="${data_json[json_item].Image}">
                        </a>
                    </div>
                  <div class="col news_icons">
                    <ul class="row list_icons">
                        <li class="col icon" ><a onclick="Share_news(\'${data_json[json_item].Guid}\')"><i class="fa-solid fa-share fa-xl"></i></a></li>
                    </ul>
                </div>
            </div>
            <div class="col-8 news_txt">
                <div class="col">
                    <text class="col news_header"><a href=${data_json[json_item].Guid}>${data_json[json_item].Title}</a></text>
                </div>
                <div class="col">
                    <text class="col news_author">${dateFormat}</text>
                </div>
                <div class="col">
                    <div class="read_more"><button class="up"><a href=${data_json[json_item].Guid}><text>Đọc tiếp</text><i class="fa-solid fa-arrow-right fa-sm"></i></button></a></div>
                    <div class="read_more"><button class="up" onclick="sum_txt(${"\'" + data_json[json_item].Guid+"\'"})"><text>Tóm tắt nội dung</text></button></div>
                    <div class="watch_later"><button class="up" onclick="Watch_later(${"\'" + data_json[json_item].Guid.toString() + "\'"}, ${"\'" + data_json[json_item].Image_content.toString().replaceAll("\'","\\'") + "\'"}, ${"\'" + data_json[json_item].Title.toString().replaceAll("\'","\\'") + "\'"}, ${"\'" + dateFormat.toString() + "\'"}, ${"\'" + data_json[json_item].Image.toString() + "\'"})"><text >Xem sau</text><i class="fa-regular fa-clock fa-sm" ></i></button></div>
                </div>
            </div>
        </div>   
        `;
      document.querySelector('.list_news').insertAdjacentHTML('beforeend', html);
    }})
  }



// var item = document.getElementById(".topic_nav_container");

//   window.addEventListener("wheel", function (e) {
//     e.preventDefault();
//     if (e.deltaY > 0) item.scrollLeft += 100;
//     else item.scrollLeft -= 100;
//   });

function Show_topic_content(content){
  let URL;
  switch (content) {
    case "tin_moi":
      URL = [`https://thanhnien.vn/rss/home.rss`];
      Load_content(URL);
      break;
    case "thoi_su":
      URL = [`https://thanhnien.vn/rss/thoi-su.rss`];
      Load_content(URL);
      break;
    case "the_gioi":
      URL = [`https://thanhnien.vn/rss/the-gioi.rss`];
      Load_content(URL);
      break;
    case "kinh_te":
      URL = [`https://thanhnien.vn/rss/kinh-te.rss`];
      Load_content(URL);
      break;
    case "doi_song":
      URL = [`https://thanhnien.vn/rss/doi-song.rss`];
      Load_content(URL);
      break;
    case "suc_khoe":
      URL = [`https://thanhnien.vn/rss/suc-khoe.rss`];
      Load_content(URL);
      break;
    case "giao_duc":
      URL = [`https://thanhnien.vn/rss/giao-duc.rss`];
      Load_content(URL);
      break
    case "the_thao":
      URL = [`https://thanhnien.vn/rss/the-thao.rss`];
      Load_content(URL);
      break
    case "du_lich":
      URL = [`https://thanhnien.vn/rss/du-lich.rss`];
      Load_content(URL);
      break
    case "xe":
      URL = [`https://thanhnien.vn/rss/xe.rss`];
      Load_content(URL);
      break
    case "giai_tri":
      URL = [`https://thanhnien.vn/rss/giai-tri.rss`];
      Load_content(URL);
      break
  }
}

addEventListener("load", (event) => {
  let URL = ['https://thanhnien.vn/rss/home.rss'];
  Load_content(URL);
});

//Chatbot popup chat
function openForm() {
  document.getElementById("popup_chat").style.display = "block";
}

function closeForm() {
  document.getElementById("popup_chat").style.display = "none";
}

function Load_content_searching(URL, keyword){
  document.querySelector('.searching_content').innerHTML = "";
  make_json(URL).then((data_json) => {
  data_json = filterIt(data_json, keyword);
    for(let json_item=0; json_item< data_json.length; json_item++)
    {
      let datetime = new Date(data_json[json_item].Publish_Date);
      //console.log(typeof(datetime));
      console.log(typeof(data_json[json_item].Guid))
      let dateFormat = datetime.getHours() + ":" + (datetime.getMinutes() < 10 ? '0' : '') + datetime.getMinutes() + ", "+ datetime.getDate() + "/" +datetime.getMonth() + "/" +datetime.getFullYear();
        let html =`
        <div class="row news">
            <div class="col-4 news_assets">
                <div class="col news_img">
                    <a href=${data_json[json_item].Guid}>
                        <img src="${data_json[json_item].Image}">
                        </a>
                    </div>
                <div class="col news_icons">
                    <ul class="row list_icons">
                        <li class="col icon" ><a onclick="Share_news(\"${data_json[json_item].Guid}\")"><i class="fa-solid fa-share fa-xl"></i></a></li>
                    </ul>
                </div>
            </div>
            <div class="col-8 news_txt">
                <div class="col">
                    <text class="col news_header"><a href=${data_json[json_item].Guid}>${data_json[json_item].Title}</a></text>
                </div>
                <div class="col">
                    <text class="col news_author">${dateFormat}</text>
                </div>
                <div class="col">
                    <div class="read_more"><button class="up"><a href=${data_json[json_item].Guid}><text>Đọc tiếp</text><i class="fa-solid fa-arrow-right fa-sm"></i></button></a></div>
                    <div class="read_more"><button class="up" onclick="sum_txt(${"\"" + data_json[json_item].Guid+"\""})"><text>Tóm tắt nội dung</text></button></div>
                    <div class="watch_later"><button class="up" onclick="Watch_later(${"\'" + data_json[json_item].Guid.toString() + "\'"}, ${"\'" + data_json[json_item].Image_content.toString().replaceAll("\'","\\'") + "\'"}, ${"\'" + data_json[json_item].Title.toString().replaceAll("\'","\\'") + "\'"}, ${"\'" + dateFormat.toString() + "\'"}, ${"\'" + data_json[json_item].Image.toString() + "\'"})"><text >Xem sau</text><i class="fa-regular fa-clock fa-sm" ></i></button></div>
                </div>
            </div>
        </div>   
        `;
      document.querySelector('#search_content').insertAdjacentHTML('beforeend', html);
    }})
  }

function filterIt(arr, searchKey) {
  return_list = []
  arr.forEach((element) => {
    if(element.Title.includes(searchKey) || element.Image_content.includes(searchKey))
    {
      return_list.push(element)
    }
  })
  return(return_list)
}

function Show_search_content(content, keyword){
  let URL;
  switch (content) {
    case "tin_moi":
      URL = [`https://thanhnien.vn/rss/home.rss`, `https://vnexpress.net/rss/tin-moi-nhat.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "thoi_su":
      URL = [`https://thanhnien.vn/rss/thoi-su.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "the_gioi":
      URL = [`https://thanhnien.vn/rss/the-gioi.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "kinh_te":
      URL = [`https://thanhnien.vn/rss/kinh-te.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "doi_song":
      URL = [`https://thanhnien.vn/rss/doi-song.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "suc_khoe":
      URL = [`https://thanhnien.vn/rss/suc-khoe.rss`];
      Load_content_searching(URL, keyword);
      break;
    case "giao_duc":
      URL = [`https://thanhnien.vn/rss/giao-duc.rss`];
      Load_content_searching(URL, keyword);
      break
    case "the_thao":
      URL = [`https://thanhnien.vn/rss/the-thao.rss`];
      Load_content_searching(URL, keyword);
      break
    case "du_lich":
      URL = [`https://thanhnien.vn/rss/du-lich.rss`];
      Load_content_searching(URL, keyword);
      break
    case "xe":
      URL = [`https://thanhnien.vn/rss/xe.rss`];
      Load_content_searching(URL, keyword);
      break
    case "giai_tri":
      URL = [`https://thanhnien.vn/rss/giai-tri.rss`];
      Load_content_searching(URL, keyword);
      break
  }
}

//Filter_search
function Search_news(content = 'tin_moi'){
  document.querySelector('.content').innerHTML = `
    <div class="topic_nav_container" id="topic_nav_container">
        <div class="topic_item" onclick="Search_news('tin_moi')">Tin mới</div>
        <div class="topic_item" onclick="Search_news('thoi_su')">Thời sự</div>
        <div class="topic_item" onclick="Search_news('the_gioi')">Thế giới</div>
        <div class="topic_item" onclick="Search_news('kinh_te')">Kinh tế</div>
        <div class="topic_item" onclick="Search_news('doi_song')">Đời sống</div>
        <div class="topic_item" onclick="Search_news('suc_khoe')">Sức khỏe</div>
        <div class="topic_item" onclick="Search_news('giao_duc')">Giáo dục</div>
        <div class="topic_item" onclick="Search_news('the_thao')">Thể thao</div>
        <div class="topic_item" onclick="Search_news('du_lich')">Du lịch</div>
        <div class="topic_item" onclick="Search_news('xe')">Xe</div>
        <div class="topic_item" onclick="Search_news('giai_tri')">Giải trí</div>
      </div>

      <div id="search_content" class="searching_content col-10 list_news" style="background-color: aqua; margin-top:0px; width: calc(95% - 100px); min-width: 300px;">
      </div>
  </div>
  `;
  Show_search_content(content, document.querySelector("#input_search").value)
}

function Share_news(url) {
  navigator.clipboard.writeText(url);
  }