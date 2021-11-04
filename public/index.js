
const sio = io({
  transportOptions: {
    polling: {
      extraHeaders: {
        'X-Username': window.location.hash.substring(1)
      }
    }
  }
});
// on VS emit
// emit : |=> send to who ? & send what ?
// on : |=> receive from who ? & receive what ?

// when client connect to server this happened :
//  #1 log connected
//  #2 send data to server at point called 'sum_data' which represent the method name
sio.on('connect', () => {
  console.log('connected');
  sio.emit('sum_data',{nums:[1,2,3]})
});

// when client disconnect from server this happened :
//  #1 log disconnected
sio.on('disconnect', () => {
  console.log('disconnected');
});

// after client connection on server he look for point called 'sum_result' and retrieve some data from it
sio.on('sum_result',(data)=>{
  // console.log(data)
  let {result} = data
  let comp=`<h3>from sum_result : ${result}</h3>`
  // console.log(result)
  document.body.insertAdjacentHTML('beforeend',comp)
})

sio.emit('mul_data',{nums:[2,4,4]},(response)=>{
  // console.log(response);
    let comp=`<h3>from mul_data : ${response}</h3>`
  // console.log(result)
  document.body.insertAdjacentHTML('beforeend',comp)

})

sio.on('sub',(data,cb)=>{
  const {numbers}=data
    let comp=`<h3>from sub : ${numbers}</h3>`
  // console.log(result)
  document.body.insertAdjacentHTML('beforeend',comp);
  cb(numbers[0]);
})

sio.on('client_count',(counter)=>{
  let comp=`<h3>client number ${counter}</h3><hr/>`
  // console.log(result)
  document.body.insertAdjacentHTML('beforeend',comp);
  console.log(`there are ${counter} total connected client`);
})

sio.on('room_count',(data)=>{
   console.log(`there are ${data} connected client with you`);
})
sio.on('user_joined',(username)=>{
  console.log(username+" joined")
})

sio.on('user_left',(username)=>{
  console.log(username+" left")
})
function get(){
  console.log('disconnected');
//   sio.on('sum_result',(data)=>{
//   console.log(data)
//   let {result} = data
//   console.log(result)
//   document.body.innerHTML+=result
// })
}
