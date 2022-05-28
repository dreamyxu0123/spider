function injectTheScript() {
  // Gets all tabs that have the specified properties, or all tabs if no properties are specified (in our case we choose current active tab)
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    // Injects JavaScript code into a page
    chrome.tabs.executeScript(tabs[0].id, { file: 'utilities.js' })
  })
}


// adding listener to your button in popup window
document.getElementById('press').addEventListener('click', async () => {
  const background = chrome.extension.getBackgroundPage()
  const context = background && background.backgroundContext
  let host = await context.getCurrentHost()
  context.log('host', host)
  context.log('host2')

  if (host == 'hpjav.tv') {
    context.hpjavDownloadVideo()
  } else if (host == 'jable.tv') {
    context.jableTvDownloadVideo()
  }
})

document.getElementById('show-url').addEventListener('click', async () => {
  const background = chrome.extension.getBackgroundPage()
  const context = background && background.backgroundContext
  const { log, request } = context
  const href = await context.getHref()
  const videoLinks = context.videoLinks[href]
  videoLinks && videoLinks.forEach((videoUrl) => {
    let element = document.createElement('div')
    // div.className = 'send-btn enable'
    element.innerHTML = videoUrl
    // element.innerHTML = url.split('/').pop()
    element.style = 'border: 1px gray solid; word-wrap: break-word;'
    element.onclick = function () {
      let host = new URL(href);
      let hostname = host.hostname
      let host_type = ''
      if (hostname == 'www2.javhdporn.net') {
        host_type = 'javhdporn'
      }
      request({ href, videoLink: videoUrl, host_type: host_type })
      alert(videoUrl)
    }
    document.body.appendChild(element)
  })
})
