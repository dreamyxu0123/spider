import requests
# var ps = document.querySelector('.entry-content').children
# var us=[]
# for (let i = 0; i < ps.length; i++) {
#   const e = ps[i].children;
#   var src = e[0].src
#   us.push(src)
# }
# console.log(us)
urls = ["https://www.moestack.com/img/2020/06/1591449783-c4ca4238a0b9238.jpg", "https://www.moestack.com/img/2020/06/1591449785-c81e728d9d4c2f6.jpg", "https://www.moestack.com/img/2020/06/1591449787-eccbc87e4b5ce2f.jpg", "https://www.moestack.com/img/2020/06/1591449790-a87ff679a2f3e71.jpg", "https://www.moestack.com/img/2020/06/1591449793-e4da3b7fbbce234.jpg", "https://www.moestack.com/img/2020/06/1591449795-1679091c5a880fa.jpg", "https://www.moestack.com/img/2020/06/1591449799-8f14e45fceea167.jpg", "https://www.moestack.com/img/2020/06/1591449802-c9f0f895fb98ab9.jpg", "https://www.moestack.com/img/2020/06/1591449804-45c48cce2e2d7fb.jpg", "https://www.moestack.com/img/2020/06/1591449807-d3d9446802a4425.jpg", "https://www.moestack.com/img/2020/06/1591449811-6512bd43d9caa6e.jpg", "https://www.moestack.com/img/2020/06/1591449815-c20ad4d76fe9775.jpg", "https://www.moestack.com/img/2020/06/1591449821-c51ce410c124a10.jpg", "https://www.moestack.com/img/2020/06/1591449828-aab3238922bcc25.jpg", "https://www.moestack.com/img/2020/06/1591449835-9bf31c7ff062936.jpg", "https://www.moestack.com/img/2020/06/1591449843-c74d97b01eae257.jpg", "https://www.moestack.com/img/2020/06/1591449851-70efdf2ec9b0860.jpg", "https://www.moestack.com/img/2020/06/1591449859-6f4922f45568161.jpg",
        "https://www.moestack.com/img/2020/06/1591449867-1f0e3dad9990834.jpg", "https://www.moestack.com/img/2020/06/1591449877-98f13708210194c.jpg", "https://www.moestack.com/img/2020/06/1591449889-3c59dc048e88502.jpg", "https://www.moestack.com/img/2020/06/1591449896-b6d767d2f8ed5d2.jpg", "https://www.moestack.com/img/2020/06/1591449905-37693cfc748049e.jpg", "https://www.moestack.com/img/2020/06/1591449914-1ff1de774005f8d.jpg", "https://www.moestack.com/img/2020/06/1591449926-8e296a067a37563.jpg", "https://www.moestack.com/img/2020/06/1591449936-4e732ced3463d06.jpg", "https://www.moestack.com/img/2020/06/1591449951-02e74f10e0327ad.jpg", "https://www.moestack.com/img/2020/06/1591449962-33e75ff09dd601b.jpg", "https://www.moestack.com/img/2020/06/1591449973-6ea9ab1baa0efb9.jpg", "https://www.moestack.com/img/2020/06/1591449985-34173cb38f07f89.jpg", "https://www.moestack.com/img/2020/06/1591449997-c16a5320fa47553.jpg", "https://www.moestack.com/img/2020/06/1591450014-6364d3f0f495b6a.jpg", "https://www.moestack.com/img/2020/06/1591450024-182be0c5cdcd507.jpg", "https://www.moestack.com/img/2020/06/1591450032-e369853df766fa4.jpg", "https://www.moestack.com/img/2020/06/1591450041-1c383cd30b7c298.jpg", "https://www.moestack.com/img/2020/06/1591450050-19ca14e7ea6328a.jpg", ]
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}


for i, v in enumerate(urls):
    r0 = requests.get(v, headers=headers)
    with open(f'imgs/img{i+1}.jpg', 'wb') as f:
        f.write(r0.content)
