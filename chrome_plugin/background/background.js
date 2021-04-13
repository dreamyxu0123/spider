const log = console.log.bind(console)
const hpjavDownloadVideo = async function () {
  let tab = await getCurrentTab()
  console.log('tabId', tab.id)
  chrome.tabs.executeScript(
    tab.id,
    {
      code: `window.location.pathname.split('/')[2]`,
    },
    (result) => {
      let videoId = result[0]
      let url = window.backgroundContext.videoLinks[videoId]
      console.log('url', url)
      Ajax(
        'post',
        'http://localhost:5000/hpjav_download',
        { url: url, filename: videoId },
        function (result) {
          alert(result)
        },
      )
    },
  )
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
  // console.log('hello url', url)
  if (url.endsWith('.m3u8', url.length)) {
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
    // chrome.tabs.executeScript(
    //   requestDetails.tabId,
    //   {
    //     code: `
    //       setTimeout(() => {
    //         let playButton = document.querySelector('.play-button')
    //         playButton.click()
    //       }, 3000)
    // `,
    //   },
    //   () => {
    //     log('Inject script success!')
    //   }
    // )
  }
  // let svg = document.querySelector('svg')
  // if (svg) {
  //   svg.click()
  // }
  // let html = `<div>${requestDetails.url}</div>`
  // appendHtml(document.body, html)
}
const M3U8_PATTERN_ARRAY = ['*://*/*']
chrome.webRequest.onBeforeRequest.addListener(logURL, {
  urls: M3U8_PATTERN_ARRAY,
})
