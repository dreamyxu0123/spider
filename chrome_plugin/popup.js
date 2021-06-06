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
  const { log, Ajax, post } = context
  const host = await context.getCurrentHost()
  const hostLinks = context.videoLinks[host]
  // context.log('context.videoLinks', context.videoLinks)
  hostLinks.forEach((url) => {
    let element = document.createElement('a')
    // div.className = 'send-btn enable'
    element.innerHTML = url.split('/').pop()
    element.onclick = function () {
      log('onclick')
      post()
    }
    document.body.appendChild(element)
  })

  // let host = await context.getCurrentHost()
  // context.log('host', host)

  // if (host == 'hpjav.tv') {
  //   context.hpjavDownloadVideo()
  // } else if (host == 'jable.tv') {
  //   context.jableTvDownloadVideo()
  // }
})
