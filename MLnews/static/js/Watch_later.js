//Chatbot popup chat
function openForm() {
    document.getElementById("popup_chat").style.display = "block";
  }
  
  function closeForm() {
    document.getElementById("popup_chat").style.display = "none";
  }

  function Load_content_searching(keyword){
    document.querySelector('.searching_content').innerHTML = "";
    console.log($('#json_test').text())
    var JSON_1 = JSON.parse($('#json_test').text())
    console.log(JSON_1)
    
    for(var i = 0; i<JSON_1.length; i++)
    {
      json_data = JSON.parse(JSON_1[i])
      if(json_data.title.includes(keyword) || json_data.image_content.includes(keyword)){
        let html =`
        <div class="row news">
            <div class="col-4 news_assets">
                <div class="col news_img">
                    <a href=${json_data.guid}>
                        <img src="${json_data.image}">
                        </a>
                    </div>
            </div>
            <div class="col-8 news_txt">
                <div class="col">
                    <text class="col news_header"><a href=${json_data.guid}>${json_data.title}</a></text>
                </div>
                <div class="col">
                    <text class="col news_author">${json_data.publised_date}</text>
                </div>
                <div class="col">
                    <text class="col news_content">${json_data.image_content}</text>
                </div>
                <div class="col">
                    <div class="read_more"><button class="up"><a href=${json_data.guid}><text>Đọc tiếp</text><i class="fa-solid fa-arrow-right fa-sm"></i></button></a></div>
                    <div class="read_more"><button class="up" onclick="sum_txt(${"\"" + json_data.guid+"\""})"><text>Tóm tắt nội dung</text></button></div>
                    <div class="watch_later"><button class="up" onclick="remove_watch_later(\'${json_data.guid}\')"><text >Xóa xem sau</text><i class="fa-regular fa-clock fa-sm" ></i></button></div>
                </div>
            </div>
        </div>   
        `
    document.querySelector("#search_content").insertAdjacentHTML("beforeend", html);
      }
      }}
  
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
  
  
  //Filter_search
  function Search_news(){
    document.querySelector('.content').innerHTML = `
    <div style=" width: 80%;display: flex; margin: auto; position: relative;" class="content">
  
        <div id="search_content" class="searching_content col-10 list_news" style="background-color: aqua; margin-top:0px; width: calc(95% - 100px); min-width: 300px;">
        </div>
    </div>
    `;
    Load_content_searching(document.querySelector("#input_search").value)
  }