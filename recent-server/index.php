<?php header("Content-Type: application/json"); header("Access-Control-Allow-Origin: *");?>
<?php
if(isset($_GET['newurlis'])){
    $json = json_decode(file_get_contents("blogs.json"));
    array_push($json, htmlspecialchars($_GET['newurlis']));
    $json = array_reverse($json);
    array_splice($json, 20);
    $json = array_reverse($json);
    file_put_contents("blogs.json", json_encode($json));
    echo json_encode($json);
} else {
    $json = file_get_contents("blogs.json");
    echo $json;
}
    
    
?>