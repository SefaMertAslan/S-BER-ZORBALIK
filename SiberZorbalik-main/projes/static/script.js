// script.js

const messageInput = document.getElementById("metin");
const sonucDiv = document.getElementById("sonuc"); // eksikti, eklendi
const result = document.getElementById("result");
const exampleCard = document.querySelector(".card:nth-child(1)");

async function analizEt() {
  const mesaj = messageInput.value;

  if (mesaj.trim() === "") {
    sonucDiv.style.display = "none";
    result.style.display = "none";
    exampleCard.style.display = "none";
    return;
  }

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: mesaj }),
  });

  const data = await response.json();
  sonucDiv.innerText = "Tahmin: " + data.tahmin;
  sonucDiv.style.display = "block";

  if (data.tahmin.toLowerCase() === "zorbalık") {
    sonucDiv.className = "alert-box alert-red";
    result.textContent = "⚠️ Bu mesaj siber zorbalık içermektedir.";
    result.className = "warning";
    result.style.display = "block";
    exampleCard.style.display = "block";
  } else {
    sonucDiv.className = "alert-box alert-green";
    result.textContent = "✅ Bu mesaj güvenlidir.";
    result.className = "safe";
    result.style.display = "block";
    exampleCard.style.display = "none";
  }

}
