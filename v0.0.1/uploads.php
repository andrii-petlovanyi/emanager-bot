<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ElxHelper</title>
    <link href="/style/style.css" rel="stylesheet" type="text/css">
</head>
<body class="body">

    <header class="header">
        
      <img src="/style/logo.png">
      <p class="logo">DownloadBD</p>
        
    </header>
    <main class="main">
    <section class="download-page">
    <?php
$target_path = "/files";
$target_path = $target_path . basename( $_FILES['uploadedfile']['name']);
if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path))
{
    echo "Нову версію БД під назвою ' ". basename( $_FILES['uploadedfile']['name']).
    "  ' успішно розміщено на сервері";
    header( "refresh:3;url=index.html" );
}
else
{
    echo "Вибачте, виникла помилка. Спробуйте ще раз!";
    header( "refresh:3;url=index.html" );
}
?>  
    </section>    
    </main>
    <footer>
        <section>(c)</section>
    </footer>

</body>
</html>



