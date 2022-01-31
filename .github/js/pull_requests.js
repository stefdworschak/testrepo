async function getData(){
  const response = await fetch(DATA_URL);
  return response.json();
}

getData().then((data) => {
  console.log(data)
})