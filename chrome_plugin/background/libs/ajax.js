const Ajax = function (method, path, data, callback) {
  let r = new XMLHttpRequest()
  // 设置请求方法和请求地址
  r.open(method, path, true)
  // 设置发送的数据的格式
  r.setRequestHeader('Content-Type', 'application/json')
  // 注册响应函数
  r.onreadystatechange = function () {
    if (r.readyState === 4) {
      // var response = JSON.parse(r.response)
      var response = r.response
      // console.log('response', response)
      callback(r.response)
    } else {
      console.log('change')
    }
  }
  // 发送请求
  data = JSON.stringify(data)
  r.send(data)
}
