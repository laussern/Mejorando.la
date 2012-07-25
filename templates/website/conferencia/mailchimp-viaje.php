<?
$nombre=$_POST['nombre'];
$apellidos=$_POST['apellidos'];
$correo=$_POST['email'];
$sexo=$_POST['sexo'];
$habitacion = $_POST['tipo'];
$telefono = $_POST['telefono'];
$twitter = $_POST['twitter'];
$comentario = $_POST['comentario'];
$ipusr = getenv('REMOTE_ADDR');

$para = 'cursos@maestrosdelweb.com';
$desde = "From: Cuarta Conferencia <cursos@maestrosdelweb.com>";
$asunto = "viaje a guatemala - Cuarta Conferencia mejorando.la";
$mensaje ='
La siguiente persona se ha inscrito:

Nombre: '.$nombre.'
Apellidos: '.$apellidos.'
E-mail: '.$correo.'
Pais/IP: '.$ipusr.'
Sexo: '.$sexo.'
Tipo de habitacion: '.$habitacion.'
Cuenta de twitter: '.$twitter.'
comentario: '.$comentario.'
';

$apikey = '05f4144fdc54b5e377dec5a4a10575de-us2';
$listId = 'a79e886005';
$ahora = strtotime("now");

 		// process here the contact form data like name and message
		mail($para, $asunto, $mensaje, $desde); // example
		//

		$merges = array('FNAME'=>$nombre,
	                	'OPTINIP'=>$ipusr,
						'OPTIN_TIME'=>$ahora
		);

		$double_optin=true;
		$update_existing=false;
		$replace_interests=true;
		$send_welcome=false;
		$email_type = 'html';            
		$data = array(
		        'email_address'=>$correo,
		        'apikey'=>$apikey,
		        'merge_vars' => $merges,
		        'id' => $listId,
		        'double_optin' => $double_optin,
		        'update_existing' => $update_existing,
		        'replace_interests' => $replace_interests,
		        'send_welcome' => $send_welcome,
		        'email_type' => $email_type
		    );
		$payload = json_encode($data);

		//replace us2 with your actual datacenter
		$submit_url = "http://us2.api.mailchimp.com/1.3/?method=listSubscribe";

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $submit_url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_POST, true);
		curl_setopt($ch, CURLOPT_POSTFIELDS, urlencode($payload));

		$result = curl_exec($ch);
		curl_close ($ch);
		$data = json_decode($result);
		if ($data->error){
		    echo $data->code .' : '.$data->error."\n";
		} else { ?>
OK
<? }

?>