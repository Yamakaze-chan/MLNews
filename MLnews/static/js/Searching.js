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
          let img = description_txt.substring(description_txt.indexOf("src=")+5).substring(0,description_txt.substring(description_txt.indexOf("src=")+5).indexOf(">")-1);
          let img_content = description_txt.substring(description_txt.indexOf("</a>")+4, description_txt.length-1).replace("</br>", "");
          //console.log(img_content);
        
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
          console.log(data_json);
      }
      }
    );
    }
    return data_json;
}

function Filter_search(json_data, keyword){
    var json_filter_data = [];
    let i = 0 ;
    json_data.forEach(element => {
        if(element.Title.includes(keyword) || element.Description.includes(keyword)){
            json_filter_data[i] = element;
            i++;
        }
    });
    return json_filter_data;
}

function Show_search_content(content, keyword){
  let URL;
  switch (content) {
    case "tin_moi":
      URL = [`https://thanhnien.vn/rss/home.rss`];
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

//Get data
function Load_content_searching(URL, keyword){
    document.querySelector('.searching_content').innerHTML = "";
    make_json(URL).then((data_json) => {
    data_json = Filter_search(data_json, keyword);
      for(let json_item=0; json_item< data_json.length; json_item++)
      {
        let datetime = new Date(data_json[json_item].Publish_Date);
        console.log(typeof(datetime));
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
                          <li class="col icon" ><a href="./LoginSignup.html"><i class="fa-regular fa-thumbs-up fa-xl"></i></a></li>
                          <!--li class="col icon"><a href="./LoginSignup.html"><i class="fa-solid fa-thumbs-up fa-xl"></i></i></a></li-->
                          <!--li class="col icon"><a href="./LoginSignup.html"><i class="fa-solid fa-thumbs-down fa-xl"></i></i></a></li-->
                          <li class="col icon" ><a href="./LoginSignup.html"><i class="fa-regular fa-thumbs-down fa-xl"></i></i></a></li>
                          <li class="col icon" ><a href="./LoginSignup.html"><i class="fa-solid fa-comment fa-xl"></i></a></li>
                          <li class="col icon" ><a href="./LoginSignup.html"><i class="fa-solid fa-share fa-xl"></i></a></li>
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
                      <div class="watch_later"><button class="up"><text >Xem sau</text><i class="fa-regular fa-clock fa-sm" ></i></button></div>
                  </div>
              </div>
          </div>   
          `;
        document.querySelector('.searching_content').insertAdjacentHTML('beforeend', html);
      }})
    }

    addEventListener("load", (event) => {
        let URL = ['https://vnexpress.net/rss/tin-moi-nhat.rss'];
        Load_content_searching(URL, "FPT");
      });
