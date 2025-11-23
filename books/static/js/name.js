const storyUrl = "https://storyclass.ai/api3";

document.addEventListener("DOMContentLoaded", function () {
  var input = document.getElementById("input-field");
  input.focus();

  

  function setWriterName() {
    var title = document.getElementById("name");
    var name = document.getElementById("input-field");

    name.addEventListener("input", function (event) {
      if (event.target.value == "") {
        title.innerHTML = `안녕하세요 ___ (이)의 보호자님!`;
      } else {
        title.innerHTML = `안녕하세요 ${event.target.value} (이)의 보호자님!`;
      }
    });
  }

  function toRequestPage() {
    var button = document.getElementById("next-button");
    var name = document.getElementById("input-field");

    button.addEventListener("click", function () {
      if (name.value === "") {
        alert("동화를 들려줄 아이의 이름을 알려주세요!");
      } else {
        sessionStorage.setItem("writer", name.value);
        window.location.href = "/start/select";
      }
    });
  }

  function getInfo() {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Accept", "application/json");

    var requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    fetch(`${storyUrl}/test`, requestOptions);
  }

  function useEffect(callback) {
    window.addEventListener("load", () => {
      callback();
    });
  }

  useEffect(() => {
    sessionStorage.setItem("edit", false);
    // getInfo();
  });

  toMyPage();
  toRequestPage();
  setWriterName();
});
