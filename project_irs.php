<?php
session_start();

// Initialize an empty array to store items
if (!isset($_SESSION['input_items'])) {
    $_SESSION['input_items'] = [];
}

// Function to add an item to the array
function add_item($length, $width, $height, $weight, $color, $qty) {
    $_SESSION['input_items'][] = [
        'length' => $length,
        'width' => $width,
        'height' => $height,
        'weight' => $weight,
        'color' => $color,
        'qty' => $qty
    ];
}

// Function to display the item table
function display_items() {
    if (!empty($_SESSION['input_items'])) {
        echo "<table>";
        echo "<tr><th>Length</th><th>Width</th><th>Height</th><th>Weight</th><th>Color</th><th>Quantity</th><th>Action</th></tr>";
        foreach ($_SESSION['input_items'] as $key => $item) {
            echo "<tr>";
            echo "<td>{$item['length']}</td>";
            echo "<td>{$item['width']}</td>";
            echo "<td>{$item['height']}</td>";
            echo "<td>{$item['weight']}</td>";
            echo "<td>{$item['color']}</td>";
            echo "<td>{$item['qty']}</td>";
            echo "<td><a href='?action=delete&key=$key'>Delete</a></td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "No items added yet.";
    }
}

// Check if form is submitted
if(isset($_POST['action'])){
   $action=$_POST['action'];
}else{
   if(isset($_GET['action'])){
      $action=$_GET['action'];
   }else{
      $action="";
   }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $length = $_POST['length'];
    $width = $_POST['width'];
    $height = $_POST['height'];
    $weight = $_POST['weight'];
    $color = $_POST['color'];
    $qty = $_POST['qty'];

    if ($action == 'add') {
        add_item($length, $width, $height, $weight, $color, $qty);
    }
}

// Check if action is delete
if ($action == 'delete') {
    $key = $_GET['key'];
    unset($_SESSION['input_items'][$key]);
}

if(isset($_POST['gen'])){
   $gen=$_POST['gen'];
}else{
   $gen="";
}

?>

    <style>
        /* Position the div */
        .positioned-div {
            position: absolute;
            top: 0px; /* Distance from the top of the page */
            left: 800px; /* Distance from the left of the page */
            width: 700px; /* Set width */
            height: 1000px; /* Set height */
        }
    </style>
	
	
<!-- Form to add an item -->
<div class="positioned-div">

<?php
// Display the item table
display_items();
?>

<form method="post" action="project_irs.php">
    <table>
        <tr>
            <td>Length</td>
            <td><input type="number" name="length"></td>
        </tr>

        <tr>
            <td>Width</td>
            <td><input type="number" name="width"></td>
        </tr>

        <tr>
            <td>Height</td>
            <td><input type="number" name="height"></td>
        </tr>

        <tr>
            <td>Weight</td>
            <td><input type="number" name="weight"></td>
        </tr>

        <tr>
            <td>Color</td>
            <td><input type="text" name="color"></td>
        </tr>

        <tr>
            <td>Quantity</td>
            <td><input type="number" name="qty"></td>
        </tr>
    </table>

    <button type="submit" name="action" value="add">Add Item</button>
	<br><br>
    <button type="submit" name="gen" value="generate">Generate Container Loading Plan</button>
</form>
</div>

</body>
</html>

<?php
if($gen=="generate"){
   $items = [];
   $cnt = 0;
   foreach ($_SESSION['input_items'] as $key => $item) {
      for($i=0; $i<$item['qty']; $i++){
         $cnt++;
	 $strcnt = (string)$cnt;

         $item_temp = [];
         $item_temp[0] = $strcnt;
		 $length = intval($item['length']);
         $item_temp[1] = $length;
		 $width = intval($item['width']);
         $item_temp[2] = $width;
		 $height = intval($item['height']);
         $item_temp[3] = $height;
		 $weight = intval($item['weight']);
         $item_temp[4] = $weight;
         $item_temp[5] = $item['color'];

         $items[] = $item_temp;
      }	
   }

   // Prepare the data as JSON
   $data = json_encode(['items' => $items]);

    // Set up cURL to call Flask application
    $ch = curl_init('localhost:5000/get_population');
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_TIMEOUT, 0);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array(
		'Content-Type: application/json',
		'Content-Length: ' . strlen($data))
	);

	// Execute the request to Flask application
	$result = curl_exec($ch);

	// Check for errors
	//if (curl_errno($ch)) {
	//   echo 'Curl error: ' . curl_error($ch);
	//}

	// Close cURL session
	curl_close($ch);

	//Output the result
	//echo $result;

	echo "<script>";
	echo "var results = " . $result . ";"; 
	echo "</script>";
?>

<canvas id="bigCanvas" width=770px height=550px style="noborder:1px solid #d3d3d3;"></canvas>

<div id="xdiv" class="cube">
<canvas id="myCanvas" width=770px height=550px style="border:1px solid #d3d3d3;"></canvas>
<script type="text/javascript">
</script>
</div>

<style>
    .cube {
    top: 0px;
    left:0px;
    position: fixed;
    }
    .bcube {
    top: 0px;
    left:0px;
    position: fixed;
    }
    .pcube {
    top: 0px;
    left:0px;
    position: fixed;
    }
    .cibox{
      top:0px;
      left:780px;
      position: fixed;
   }
    .ciremark{
      top:0px;
      left:1070px;
      position: fixed;
   }
    .bfl {
    top: 0px;
    left:0px;
    position: fixed;
    }
    .ccollect {
    top:70px;
    left:780px;
    position:fixed;
    font-size: 10pt;
    }
    .climit{
      top:460px;
      left:530px;
      position: fixed;
      font-size: 12pt;
   }
    .clcont{
      top:586px;
      /*top:560px;*/
      left:10px;
      position: fixed;
      font-size: 20pt;
   }
    .clset{
      top:50px;
      left:783px;
      position: fixed;
      font-size: 10pt;
   }
    .cid{
      top:700px;
      /*top:600px;*/
      left:10px;
      position: fixed;
      font-size: 12pt;
   }
textarea { vertical-align: top; }
</style>

<div class="climit" id="divlimit">
Container <input id="idcontsize" type="text" name="idcontsize" size=25 readonly style="font-size: 11px; text-align:left;"><br>
Qty Items <input id="qtyitem" type="text" name="qtyitem" size=5 readonly style="font-size: 11px; text-align:right;"><br>
Volume <input id="idperc" type="text" name="idperc" size=5 readonly style="font-size: 11px; text-align:right;"> %<br>
</div>

<script type="text/javascript" language="javascript" src="js/jquery-1.4.2.min.js"></script>
<script type="text/javascript">

function addcont(){

	vjumactcont = 1;
	vjumcont = 1;
	vunit="divcont"+vjumcont;
	vtxt="var "+vunit+"= document.createElement('div');";
	eval(vtxt);
	eval(vunit).id=vunit;
	eval(vunit).className="pcube";
	eval(vunit).style.width=770;
	eval(vunit).style.height=550;
	document.body.appendChild(eval(vunit));

	vnamecont="mycont"+vjumcont;
	vtxt="var "+vnamecont+" = document.createElement('canvas');";
	eval(vtxt);
	div = document.getElementById(vunit);
	eval(vnamecont).id     = vnamecont;
	eval(vnamecont).width  = 770;
	eval(vnamecont).height = 550;
	eval(vunit).appendChild(eval(vnamecont));

	var ctx = eval(vnamecont).getContext("2d");

  	clength[vjumactcont]=12050;
  	cwidth[vjumactcont]=2320;
  	cheight[vjumactcont]=2250;


	//depan
	x8=649;
	y8=165.3481794490;

	x7=x8+(cwidth[vjumactcont]/vratio);
	y7=y8-(Math.tan(vdegdepan*Math.PI/180)*(x8-x7))

	ctx.moveTo(x8,y8);
	ctx.lineTo(x7,y7);

	x3=x7-(clength[vjumactcont]/vratiosamping);
	y3=y7-(Math.tan(vdegsamping*Math.PI/180)*(x7-x3));
	ctx.lineTo(x3,y3);

	x2=x3;
	y2=y3-(cheight[vjumactcont]/vratio);
	ctx.lineTo(x2,y2);

	x1=x2-(cwidth[vjumactcont]/vratio);
	y1=y2-(Math.tan(vdegdepan*Math.PI/180)*(x2-x1));
	ctx.lineTo(x1,y1);

	x4=x1;
	y4=(cheight[vjumactcont]/vratio)+y1;
	ctx.lineTo(x4,y4);

	x5=x1+(clength[vjumactcont]/vratiosamping);
	y5=(Math.tan(vdegsamping*Math.PI/180)*(x5-x1))+y1;
	ctx.moveTo(x8,y8);
	ctx.lineTo(x5,y5);

	x6=(cwidth[vjumactcont]/vratio)+x5;
	y6=(Math.tan(vdegdepan*Math.PI/180)*(x6-x5))+y5;
	ctx.lineTo(x6,y6);
	ctx.lineTo(x7,y7);

	ctx.moveTo(x4,y4);
	ctx.lineTo(x3,y3);
	ctx.moveTo(x4,y4);
	ctx.lineTo(x8,y8);
	ctx.moveTo(x1,y1);
	ctx.lineTo(x5,y5);
	ctx.moveTo(x2,y2);
	ctx.lineTo(x6,y6);
	ctx.stroke();

	vmulaix=x1;
	vmulaiy=y1;

	ctx.moveTo(x5,y5);
	//pintu depan kiri
	vdeg=vdegdepan+35;

	ctx.beginPath();
	xMe=vmulaix;
	yMe=vmulaiy;
	xp1=((cwidth[vjumactcont]/vratio)/4)+vmulaix;
	yp1=(Math.tan(vdeg*Math.PI/180)*(xp1-xMe))+yMe;
	    ctx.moveTo(vmulaix,vmulaiy);
	    ctx.lineTo(xp1,yp1);

	xp2=xp1;
	yp2=(cheight[vjumactcont]/vratio)+yp1;
	    ctx.lineTo(xp2,yp2);
	    ctx.lineTo(x4,y4);
	    ctx.lineTo(vmulaix,vmulaiy);

	    ctx.closePath();
	    ctx.stroke();
	    ctx.fillStyle="rgba(0,0,0,0.5)";
	    ctx.fill();

	//pintu depan kanan
	vdeg=vdeg+120;
	ctx.beginPath();
	xMe=x2;
	yMe=y2;
	xp3=xMe-((cwidth[vjumactcont]/vratio)/1.7);
	yp3=(Math.tan(vdeg*Math.PI/180)*(xp3-xMe))+yMe;
	    ctx.moveTo(x2,y2);
	    ctx.lineTo(xp3,yp3);

	xp4=xp3;
	yp4=(cheight[vjumactcont]/vratio)+yp3;
	    ctx.lineTo(xp4,yp4);
	    ctx.lineTo(x3,y3);
	    ctx.lineTo(x2,y2);

	    ctx.closePath();
	    ctx.stroke();
	    ctx.fillStyle="rgba(0,0,0,0.5)";
	    ctx.fill();
}


function addbox(blength, bwidth, bheight, bcolor, posx, posy){
	var ctx = eval(vnamecont).getContext("2d");

	x8=posx;
	y8=posy;

	x7=x8+(bwidth/vratio);
	y7=y8-(Math.tan(vdegdepan*Math.PI/180)*(x8-x7))

	x3=x7-(blength/vratiosamping);
	y3=y7-(Math.tan(vdegsamping*Math.PI/180)*(x7-x3));

	x2=x3;
	y2=y3-(bheight/vratio);

	x1=x2-(bwidth/vratio);
	y1=y2-(Math.tan(vdegdepan*Math.PI/180)*(x2-x1));


	x4=x1;
	y4=(bheight/vratio)+y1;

	x5=x1+(blength/vratiosamping);
	y5=(Math.tan(vdegsamping*Math.PI/180)*(x5-x1))+y1;

	x6=(bwidth/vratio)+x5;
	y6=(Math.tan(vdegdepan*Math.PI/180)*(x6-x5))+y5;

	ctx.beginPath();
	ctx.moveTo(x8,y8);
	ctx.lineTo(x7,y7);
	ctx.lineTo(x3,y3);
	ctx.lineTo(x4,y4);
	ctx.lineTo(x8,y8);
	ctx.stroke();
	ctx.closePath();
	ctx.globalAlpha = 0.5;
    ctx.fillStyle=bcolor;
    ctx.fill();

	ctx.beginPath();
	ctx.moveTo(x3,y3);
	ctx.lineTo(x2,y2);
	ctx.lineTo(x1,y1);
	ctx.lineTo(x4,y4);
	ctx.stroke();
	ctx.closePath();
	ctx.globalAlpha = 0.5;
    ctx.fillStyle=bcolor;
    ctx.fill();

	ctx.beginPath();
	ctx.moveTo(x8,y8);
	ctx.lineTo(x5,y5);
	ctx.lineTo(x6,y6);
	ctx.lineTo(x7,y7);
	ctx.stroke();
	ctx.closePath();
	ctx.globalAlpha = 0.5;
    ctx.fillStyle=bcolor;
    ctx.fill();
	
	ctx.beginPath();
	ctx.moveTo(x4,y4);
	ctx.lineTo(x8,y8);
	ctx.lineTo(x5,y5);
	ctx.lineTo(x1,y1);
	ctx.stroke();
    ctx.closePath();
	ctx.globalAlpha = 0.5;
    ctx.fillStyle=bcolor;
    ctx.fill();

	ctx.moveTo(x2,y2);
	ctx.lineTo(x6,y6);
	ctx.lineTo(x5,y5);
	ctx.stroke();

	ctx.moveTo(x1,y1);
	ctx.lineTo(x2,y2);
	ctx.lineTo(x3,y3);
	ctx.lineTo(x4,y4);
	ctx.stroke();

	ctx.moveTo(x5,y5);
	ctx.lineTo(x6,y6);
	ctx.lineTo(x7,y7);
	ctx.lineTo(x8,y8);
	ctx.stroke();

	ctx.moveTo(x1,y1);
	ctx.lineTo(x5,y5);
	ctx.stroke();

	ctx.moveTo(x2,y2);
	ctx.lineTo(x6,y6);
	ctx.stroke();

	ctx.moveTo(x3,y3);
	ctx.lineTo(x7,y7);
	ctx.stroke();

	ctx.moveTo(x4,y4);
	ctx.lineTo(x8,y8);
	ctx.stroke();

}

function calc_loc(blength, bwidth, bheight, vi){
	x8=vposx_init;
	y8=vposy_init;

	x7=x8+(bwidth/vratio);
	y7=y8-(Math.tan(vdegdepan*Math.PI/180)*(x8-x7))

	x3=x7-(blength/vratiosamping);
	y3=y7-(Math.tan(vdegsamping*Math.PI/180)*(x7-x3));

	x2=x3;
	y2=y3-(bheight/vratio);

	x1=x2-(bwidth/vratio);
	y1=y2-(Math.tan(vdegdepan*Math.PI/180)*(x2-x1));


	x4=x1;
	y4=(bheight/vratio)+y1;

	x5=x1+(blength/vratiosamping);
	y5=(Math.tan(vdegsamping*Math.PI/180)*(x5-x1))+y1;

	x6=(bwidth/vratio)+x5;
	y6=(Math.tan(vdegdepan*Math.PI/180)*(x6-x5))+y5;

//if(vi==1){
//	alert("Dim : "+blength+" x "+bwidth+" x "+bheight+" X1: "+x1+" Y1: "+y1+", X2: "+x2+" Y2: "+y2+", X3: "+x3+" Y3: "+y3+", X4: "+x4+" Y4: "+y4+", X5: "+x5+" Y5: "+y5+", X6: "+x6+" Y6: "+y6+", X7: "+x7+" Y7: "+y7+", X8: "+x8+" Y8: "+y8);
//}

	return [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8];
}

function roundToTwo(num) {
    return +(Math.round(num + "e+2")  + "e-2");
}


//main program
var clength = new Array(100);
var cwidth = new Array(100);
var cheight = new Array(100);
vratio=20;
vratiosamping=20;

vdegdepan=25;
vdegsamping=-26;


addcont();
idcontsize.value="40HC "+clength[vjumactcont]+" x "+cwidth[vjumactcont]+" x "+cheight[vjumactcont];

vposx_init=649;
vposy_init=165.3481794490;

rlength=results.length;
var i = 0
var vtotalvolume=0;
while(i<rlength){
	var [vx1, vy1, vx2, vy2, vx3, vy3, vx4, vy4, vx5, vy5, vx6, vy6, vx7, vy7, vx8, vy8] = calc_loc(results[i][6], results[i][7], results[i][8], i)

	if(results[i][5]==0){
		vlength=results[i][1];
		vwidth=results[i][2];
		vheight=results[i][3];
	}else{
		vlength=results[i][2];
		vwidth=results[i][1];
		vheight=results[i][3];
	}

	vcolor=results[i][9];

	posx=vposx_init;
	posy=vposy_init;
	addbox(vlength, vwidth, vheight, vcolor, vx2, vy2);

	vtotalvolume = vtotalvolume + (vlength*vwidth*vheight);
	i++;
}
qtyitem.value=i+" pcs";
idperc.value=roundToTwo(((vtotalvolume/(clength[vjumactcont]*cwidth[vjumactcont]*cheight[vjumactcont]))*100));

</script>

<?php
}
?>
