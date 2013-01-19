<?php

//database settings
$db = new PDO('mysql:host=localhost;dbname=playtest;charset=utf8', 'root', 'password');

//validate
if( is_numeric($_GET['from']) &&
    is_numeric($_GET['to']) &&
    is_numeric($_GET['time']) &&
    is_numeric($_GET['score']) &&
    is_numeric($_GET['down']) &&
    is_numeric($_GET['togo']) &&
    strlen($_GET['off']) <= 3 &&
    strlen($_GET['def']) <= 3) {

    $from = $_GET['from'];
    $to = $_GET['to'];
    $off = $_GET['off'];
    $def = $_GET['def'];
    $time = $_GET['time'];
    $score = $_GET['score'];
    $down = $_GET['down'];
    $togo = $_GET['togo'];
    
    $where = "where season>=? and season<=?";
    if($off != '0') $where .= " and offense=?";
    if($def != '0') $where .= " and defense=?";
    switch($time) {
        case '0':
            break;
        case '1':
            $where .= " and quarter<=2";
            break;
        case '2':
            $where .= " and quarter>2 and quarter<=4";
            break;
        case '3':
            $where .= " and quarter=4 and minutes<6";
            break;
        case '4':
            $where .= " and quarter=4 and minutes<3";
            break;
        case '5':
            $where .= " and quarter=5";
            break;
    }
    switch($score) {
        case '0':
            break;
        case '1':
            $where .= " and scorediff>=1 and scorediff<=8";
            break;
        case '2':
            $where .= " and scorediff>=9 and scorediff<=16";
            break;
        case '3':
            $where .= " and scorediff>=17";
            break;
        case '4':
            $where .= " and scorediff<=-1 and scorediff>=-8";
            break;
        case '5':
            $where .= " and scorediff<=-9 and scorediff>=-16";
            break;
        case '6':
            $where .= " and scorediff<=-17";
            break;
        case '7':
            $where .= " and scorediff=0";
            break;
    }
    switch($down) {
        case '0':
            break;
        case '1':
            $where .= " and down=1";
            break;
        case '2':
            $where .= " and down=2";
            break;
        case '3':
            $where .= " and down=3";
            break;
        case '4':
            $where .= " and down=4";
            break;
    }
    switch($togo) {
        case '0':
            break;
        case '1':
            $where .= " and togo>=11";
            break;
        case '2':
            $where .= " and togo=10";
            break;
        case '3':
            $where .= " and togo>=5 and togo<=10";
            break;
        case '4':
            $where .= " and togo>=1 and togo<=5";
            break;
        case '5':
            $where .= " and togo>=1 and togo<=2";
            break;
        case '6':
            $where .= " and togo=1";
            break;
    }
    
    try {
        $return = array();
        //get drive histogram
        if($down == '0' && $togo == '0') {
            $s = $db->prepare("select result as 'r',count(result) as 'c' from plays ".$where." and result!='play' group by result order by result;");
            $i = 1;
            $s->bindValue($i,$from,PDO::PARAM_INT); $i++;
            $s->bindValue($i,$to,PDO::PARAM_INT); $i++;
            if($off != '0') { $s->bindValue($i,$off,PDO::PARAM_STR); $i++; }
            if($def != '0') { $s->bindValue($i,$def,PDO::PARAM_STR); $i++; }
            $s->execute();
            $rows = $s->fetchAll(PDO::FETCH_ASSOC);
            $return['results'] = $rows;
        }
        //play stats
        $s = $db->prepare("select playtype as 'type',count(playtype) as 'plays',sum(success) as 'success' from plays ".$where." and (playtype='pass' or playtype='run') group by playtype order by playtype");
        $i = 1;
        $s->bindValue($i,$from,PDO::PARAM_INT); $i++;
        $s->bindValue($i,$to,PDO::PARAM_INT); $i++;
        if($off != '0') { $s->bindValue($i,$off,PDO::PARAM_STR); $i++; }
        if($def != '0') { $s->bindValue($i,$def,PDO::PARAM_STR); $i++; }
        $s->execute();
        $rows = $s->fetchAll(PDO::FETCH_ASSOC);
        $return['plays'] = $rows;
        
        //play histograms
        $s = $db->prepare("select playtype as 'type',yards,count(yards) as 'c' from plays ".$where." and (playtype='pass' or playtype='run') group by yards,playtype");
        $i = 1;
        $s->bindValue($i,$from,PDO::PARAM_INT); $i++;
        $s->bindValue($i,$to,PDO::PARAM_INT); $i++;
        if($off != '0') { $s->bindValue($i,$off,PDO::PARAM_STR); $i++; }
        if($def != '0') { $s->bindValue($i,$def,PDO::PARAM_STR); $i++; }
        $s->execute();
        $rows = $s->fetchAll(PDO::FETCH_ASSOC);
        $return['yards'] = $rows;
        
        echo json_encode($return);
    }
    catch (PDOException $ex) { echo '{"error":2}'; }
    

    
}
else {
    echo '{"error":1}';
}
?>
