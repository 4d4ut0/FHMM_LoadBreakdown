package com.testobject.httprequest;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.util.Log;
import android.view.ContextThemeWrapper;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;

import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.testobject.httprequest.respJsonInstaller.respJsonInstaller;
import com.testobject.httprequest.respJsonLogin.Perfil;
import com.testobject.httprequest.respJsonLogin.Result;
import com.testobject.httprequest.respJsonLogin.respJsonLogin;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

import static java.lang.Thread.sleep;

public class InstallerActivity extends AppCompatActivity {
    private static final int REQUEST_SIGNUP = 0;
    private respJsonLogin respJson;
    private respJsonInstaller installer;
    static String ipWoxintonn = "http://nexsolar.sytes.net/ceb/api/Usuario/ObterUsuarioPorPerfil";
    private ProgressDialog progressDialog;
    private String cookieName;
    private String cookieValue;
    private ListView lv;
    private ArrayAdapter<String> adapter;
    private EditText inputSearch;
    private AlertDialog.Builder userDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_installer);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        if (bundle != null){
            respJson = (respJsonLogin) getIntent().getSerializableExtra("json");
            cookieName = (String) getIntent().getSerializableExtra("cookieName");
            cookieValue = (String) getIntent().getSerializableExtra("cookieValue");
            Log.v("msg", Integer.toString(respJson.getResult().getIdUsuario()));
            Log.v("name", cookieName);
            Log.v("value", cookieValue);
        }

        getUserList();

        lv = findViewById(R.id.list_view);

        lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                //startUserDialog(installer.getAllNameUser().get(i),installer.getAllIdUser().get(i));
                sendUserDashBoard(installer.getAllIdUser().get(i), installer.getAllNameUser().get(i), installer.getAllStatusUser().get(i));
            }
        });

    }

    public respJsonInstaller post(){
        try {
            final java.net.URL url = new URL(ipWoxintonn);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            String cookie = cookieName + "=" + cookieValue +"; domain=192.168.0.30";
            connection.setRequestProperty("Cookie", cookie);
            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Log.v("meuuuuu, amigo", oloco);
            respJsonInstaller msg = new Gson().fromJson(oloco, respJsonInstaller.class);
            return msg;
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }

        return null;
    }

    public void getUserList(){
        Thread thread = new Thread(new Runnable() {

            @Override
            public void run() {
               installer = post();
               List<String> allNames = installer.getAllNameUser();
                for(int i = 0; i < installer.getAllIdUser().size(); i++) {
                    Log.v(Integer.toString(i), installer.getAllNameUser().get(i) );
                }
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        List<String> allNames = installer.getAllNameUser();
                        adapter = new ArrayAdapter<>(InstallerActivity.this, R.layout.list_item, R.id.product_name, allNames);
                        lv.setAdapter(adapter);
                    }
                });
            }
        });
        thread.start();
    }

    public void startUserDialog(final String name, final Integer idUsuario){
        userDialog= new AlertDialog.Builder(new ContextThemeWrapper(this, R.style.MyDialog));
        userDialog.setTitle(name);
        userDialog.setMessage("Sabiamente o caminho, escolher, voce deve!! xD");

        userDialog.setPositiveButton("Monitorar", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                sendMonitoramento(idUsuario, name);
            }
        });
        userDialog.setNeutralButton("Nova Estação", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                sendNewDV(idUsuario, name);
            }
        });
        userDialog.setNegativeButton("Novo Horimetro", new DialogInterface.OnClickListener(){
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                sendNewHor(idUsuario,name);
            }
        });
        AlertDialog alerta = userDialog.create();
        alerta.show();
    }

    public void sendNewDV(Integer id, String name){
        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("userName", name);
        bundle.putInt("userId", id);
        bundle.putString("cookieName", cookieName);
        bundle.putString("cookieValue", cookieValue);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);
    }

    public void sendMonitoramento(Integer id, String name){
        Intent intent = new Intent(getApplicationContext(), UserConsumoActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("userName", name);
        bundle.putInt("userId", id);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);
    }

    public void sendNewHor(Integer id,String name){
        Intent intent = new Intent(getApplicationContext(), MainOrimetroActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("userName", name);
        bundle.putInt("userId", id);
        bundle.putString("cookieName", cookieName);
        bundle.putString("cookieValue", cookieValue);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);
    }

    public void sendUserDashBoard(Integer id, String name, Boolean status){
        respJsonLogin userJson = new respJsonLogin();
        Result result = new Result();
        Perfil perfil = new Perfil();
        result.setIdUsuario(id);
        result.setNome(name);
        result.setCpf("PRIVADO");
        result.setAtivo(status);
        perfil.setNome("CLIENTE");
        perfil.setDescricao("");
        result.setPerfil(perfil);
        userJson.setResult(result);


        Intent intent = new Intent(getApplicationContext(), UserActivity.class);
        Bundle bundle = new Bundle();
        bundle.putSerializable("json", userJson);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);

    }

}
