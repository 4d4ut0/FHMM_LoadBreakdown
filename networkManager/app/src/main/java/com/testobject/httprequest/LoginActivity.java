package com.testobject.httprequest;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.util.Log;

import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.testobject.httprequest.respJsonLogin.respJsonLogin;

import org.json.JSONObject;

import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpCookie;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Map;

import butterknife.ButterKnife;
import butterknife.BindView;


public class LoginActivity extends AppCompatActivity {
    private static final String TAG = "LoginActivity";
    private static final int REQUEST_SIGNUP = 0;
    static String ipWoxintonn = "http://nexsolar.sytes.net/ceb/api/usuario/logar";
    private ProgressDialog progressDialog;
    private AlertDialog.Builder errorDialog;
    private respJsonLogin respJson;
    private String cookieName;
    private String cookieValue;

    @BindView(R.id.input_email) EditText _emailText;
    @BindView(R.id.input_password) EditText _passwordText;
    @BindView(R.id.btn_login) Button _loginButton;
    @BindView(R.id.link_signup) TextView _signupLink;
    JSONObject manJson = new JSONObject();

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        ButterKnife.bind(this);

        _loginButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                login();
            }
        });

        _signupLink.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                // Start the Signup activity
                Intent intent = new Intent(getApplicationContext(), SignupActivity.class);
                startActivityForResult(intent, REQUEST_SIGNUP);
            }
        });
    }

    public void login() {
        Log.d(TAG, "Login");
        if (!validate()) {
            onValidateFailed();
            return;
        }

        startDialog("Autenticando", "Buscando servidor...");

        autenticationLogin();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_SIGNUP) {
            if (resultCode == RESULT_OK) {

                // TODO: Implement successful signup logic here
                // By default we just finish the Activity and log them in automatically
                this.finish();
            }
        }
    }

    @Override
    public void onBackPressed() {
        // disable going back to the MainActivity
        moveTaskToBack(true);
    }

    public void onLoginSuccess() {
        progressDialog.dismiss();
        if(respJson.getResult().getPerfil().getNome().toLowerCase().equals("cliente")){
            Intent intent = new Intent(getApplicationContext(), UserActivity.class);
            Bundle bundle = new Bundle();
            bundle.putSerializable("json", respJson);
            intent.putExtras(bundle);
            startActivityForResult(intent, REQUEST_SIGNUP);
        }
        else if(respJson.getResult().getPerfil().getNome().toLowerCase().equals("instalador")){
            Intent intent = new Intent(getApplicationContext(), InstallerActivity.class);
            Bundle bundle = new Bundle();
            bundle.putSerializable("json", respJson);
            bundle.putString("cookieName", cookieName);
            bundle.putString("cookieValue", cookieValue);
            intent.putExtras(bundle);
            startActivityForResult(intent, REQUEST_SIGNUP);
        }
        else{
            startErrorDialog("Administrador...", "Você ainda não tem seu proprio app, mas se você acreditar um dia vai! xD");
        }
        //finish();
    }

    public void onLoginFailed() {
        progressDialog.dismiss();

        this.runOnUiThread(new Runnable() {
            public void run() {
                if(respJson == null)
                    startErrorDialog("Servidor não encontrado", "Verifique sua conexão ou entre em contato com o suporte");
                else
                    startErrorDialog("Erro ao autenticar :'(",respJson.getMessage()+" Verifique seus dados e tente novamento, nós acreditamos em vc!!!");
            }
        });
    }

    public boolean validate() {
        boolean valid = true;

        String email = _emailText.getText().toString();
        String password = _passwordText.getText().toString();

        if (email.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            _emailText.setError("enter a valid email address");
            valid = false;
        } else {
            _emailText.setError(null);
        }

        if (password.isEmpty() || password.length() < 4 || password.length() > 10) {
            _passwordText.setError("between 4 and 10 alphanumeric characters");
            valid = false;
        } else {
            _passwordText.setError(null);
        }

        return valid;
    }

    public respJsonLogin post(final JSONObject data){
        try {
            final java.net.URL url = new URL(ipWoxintonn);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestProperty("Content-type", "application/json");
            connection.setRequestMethod("POST");
            connection.setDoInput(true);
            connection.setDoOutput(true);

            final OutputStream outputStream = connection.getOutputStream();
            final BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));

            writer.write(data.toString());
            writer.flush();
            writer.close();
            outputStream.close();

            connection.connect();

            Map<String, List<String>> headerFields = connection.getHeaderFields();
            List<String> cookiesHeader = headerFields.get("Set-Cookie");
            if(cookiesHeader != null){
                String cookie = cookiesHeader.get(0);
                HttpCookie httpCookie = HttpCookie.parse(cookie).get(0);
                cookieName = httpCookie.getName();
                cookieValue = httpCookie.getValue();
            }
            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            respJsonLogin msg = new Gson().fromJson(oloco, respJsonLogin.class);
            progressDialog.dismiss();
            return msg;
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }

        return null;
    }

    public void startDialog(String title, String msg){
        progressDialog = new ProgressDialog(LoginActivity.this);
        progressDialog.setIndeterminate(true);
        progressDialog.setTitle(title);
        progressDialog.setMessage(msg);
        progressDialog.setCanceledOnTouchOutside(false);
        progressDialog.setMax(100);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
    }

    public void startErrorDialog(String title, String msg){
        errorDialog= new AlertDialog.Builder(this);
        errorDialog.setTitle(title);
        errorDialog.setMessage(msg);
        errorDialog.setPositiveButton("OK", null);
        AlertDialog alerta = errorDialog.create();
        alerta.show();
    }

    public void autenticationLogin(){
        Thread thread = new Thread(new Runnable() {

            @Override
            public void run() {
                try  {
                    String email = _emailText.getText().toString();
                    String password = _passwordText.getText().toString();
                    manJson.put("email", email);
                    manJson.put("senha", password);

                    respJson = post(manJson);
                    Log.v("json", manJson.toString());
                    if(respJson != null){
                        if(respJson.getMessage() == null)
                            onLoginSuccess();
                        else//tratar todos os tipos de erro de login
                            onLoginFailed();
                    }
                    else onLoginFailed();

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }

    public void onValidateFailed(){
        Toast.makeText(getBaseContext(), "Login failed", Toast.LENGTH_LONG).show();
    }
}