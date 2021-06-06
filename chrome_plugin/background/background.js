const log = console.log.bind(console)

const hpjavDownloadVideo = async function () {
  let code = `window.location.pathname.split('/')[2]`
  let result = await executeScript(code)
  let videoId = result[0]
  let url = window.backgroundContext.videoLinks[videoId]
  let video_type = url.split('.').pop()
  // log('url', url)
  Ajax(
    'post',
    'http://127.0.0.1:5000/hpjav_download',
    { url: url, filename: videoId, video_type },
    function (result) {
      alert(result)
    },
  )
}
const executeScript = async function (code) {
  let tab = await getCurrentTab()
  return new Promise((resolve, reject) => {
    chrome.tabs.executeScript(tab.id, { code: code }, (result) => {
      resolve(result)
    })
  })
}

const jableTvDownloadVideo = async function () {
  let tab = await getCurrentTab()
  chrome.tabs.executeScript(
    tab.id,
    {
      code: `window.location.href`,
    },
    (result) => {
      let url = result[0]
      Ajax(
        'post',
        'http://localhost:5000/jable_tv_download',
        { url: url },
        function (result) {
          alert(result)
        },
      )
    },
  )
}

const getCurrentHost = async function () {
  let tab = await getCurrentTab()
  return new Promise((resolve) => {
    chrome.tabs.executeScript(
      tab.id,
      {
        code: `window.location.host`,
      },
      (result) => {
        resolve(result[0])
      },
    )
  })
}

function getCurrentTab() {
  return new Promise((resolve) =>
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) =>
      resolve(tabs[0]),
    ),
  )
}
window['backgroundContext'] = {
  log: console.log.bind(console),
  videoLinks: {},
  hpjavDownloadVideo,
  jableTvDownloadVideo,
  getCurrentHost,
}

let appendHtml = function (element, html) {
  element.insertAdjacentHTML('beforeend', html)
}

let logURL = function (requestDetails) {
  let url = requestDetails.url
  // log('logURL url', url)
  let bool =
    url.endsWith('.m3u8', url.length) || url.endsWith('720p.mp4', url.length)
  if (bool) {
    chrome.tabs.executeScript(
      requestDetails.tabId,
      {
        code: `window.location.pathname.split('/')[2]`,
      },
      (result) => {
        window.backgroundContext.videoLinks[result[0]] = url
      },
    )
    console.log('hello url', url)
  }
}
const M3U8_PATTERN_ARRAY = ['*://*/*']
chrome.webRequest.onBeforeRequest.addListener(logURL, {
  urls: M3U8_PATTERN_ARRAY,
})
