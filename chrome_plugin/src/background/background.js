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
      // log('executeScript code', code, 'result', result)
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

const getCurrentTab = function () {
  return new Promise((resolve) =>
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(tabs[0])
    }),
  )
}

const getHref = async function () {
  const code = `window.location.href`
  const href = await executeScript(code)
  return href[0]
}
const javhdporn = function (data) {
  Ajax('POST', 'http://localhost:5000/javhdporn', data, (response) => {
    log('response', response)
  })
}

const request = function (requestData) {
  let { videoLink, href, host_type } = requestData
  if (host_type == 'javhdporn') {
    javhdporn(requestData)
    return
  }
  let videoType = ''
  if (
    videoLink.endsWith('.m3u8', videoLink.length) ||
    videoLink.search('.m3u8') != -1
  ) {
    videoType = 'm3u8'
  } else {
    videoType = 'mp4'
  }
  log('videoType', videoType)
  const data = {
    video_link: videoLink,
    page_url: href,
    video_type: videoType,
  }
  Ajax('POST', 'http://localhost:5000/', data, (response) => {
    log('response', response)
  })
}
window['backgroundContext'] = {
  log: console.log.bind(console),
  videoLinks: {},
  hpjavDownloadVideo,
  jableTvDownloadVideo,
  getCurrentHost,
  getHref,
  request,
}

const appendHtml = function (element, html) {
  element.insertAdjacentHTML('beforeend', html)
}
const bodyOnload = function () {
  Object.prototype.__defineGetter__ = null
  document.querySelector('.play-button').click()
  document.domain = 'blob:https://www2.javhdporn.net'
  setTimeout(() => {
    document.querySelector('.jw-display-icon-container').click()
  }, 1000)
}
const logURL = async function (requestDetails) {
  // const code = `document.body.onload = ${bodyOnload.toString()}`
  // await executeScript(code)
  let url = requestDetails.url
  // log('logURL url', url)
  let bool =
    url.endsWith('.m3u8', url.length) ||
    url.endsWith('720p.mp4', url.length) ||
    url.search('.m3u8') != -1 ||
    url.search('.mp4') != -1
  if (bool) {
    const href = await getHref()
    // log('log url href', href)
    // window.backgroundContext.videoLinks[href] = url
    const videoLinks = window.backgroundContext.videoLinks
    if (videoLinks[href]) {
      if (!videoLinks[href].includes(url)) {
        videoLinks[href].push(url)
      }
    } else {
      videoLinks[href] = [url]
    }
  }
}
const M3U8_PATTERN_ARRAY = ['*://*/*']
chrome.webRequest.onBeforeRequest.addListener(logURL, {
  urls: M3U8_PATTERN_ARRAY,
})

