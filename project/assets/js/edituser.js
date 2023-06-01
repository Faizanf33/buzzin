document.getElementById("user_image").addEventListener("change", (e) => {
    let profile_img = document.getElementById("profile_img");
  
    let img_path = e.target.files[0];
    console.log(img_path);
    let img_type = img_path.type;
    if (img_type.match(/image.*/)) {
        let img_url = URL.createObjectURL(img_path);
        profile_img.src = img_url;
    }
    else {
      e.target.value="";
        }
});
