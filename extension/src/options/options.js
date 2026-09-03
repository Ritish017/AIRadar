// Options page logic

const apiUrlInput = document.getElementById("api-url");
const aiModelSelect = document.getElementById("ai-model");
const minScoreInput = document.getElementById("min-score");
const scoreValSpan = document.getElementById("score-val");
const prefToneSelect = document.getElementById("pref-tone");
const saveBtn = document.getElementById("btn-save");
const saveToast = document.getElementById("save-toast");

// Load stored settings
chrome.storage.local.get(["apiUrl", "aiModel", "minViralScore", "preferredTone"], (res) => {
  if (res.apiUrl) apiUrlInput.value = res.apiUrl;
  if (res.aiModel) aiModelSelect.value = res.aiModel;
  if (res.minViralScore) {
    minScoreInput.value = res.minViralScore;
    scoreValSpan.innerText = res.minViralScore;
  }
  if (res.preferredTone) prefToneSelect.value = res.preferredTone;
});

minScoreInput.addEventListener("input", (e) => {
  scoreValSpan.innerText = e.target.value;
});

saveBtn.addEventListener("click", () => {
  chrome.storage.local.set({
    apiUrl: apiUrlInput.value.trim(),
    aiModel: aiModelSelect.value,
    minViralScore: parseInt(minScoreInput.value, 10),
    preferredTone: prefToneSelect.value
  }, () => {
    saveToast.style.display = "inline";
    setTimeout(() => {
      saveToast.style.display = "none";
    }, 2000);
  });
});
