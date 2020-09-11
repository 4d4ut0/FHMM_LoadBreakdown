package com.testobject.httprequest;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import com.google.android.material.textfield.TextInputEditText;
import androidx.appcompat.app.AppCompatActivity;

import android.os.SystemClock;
import android.provider.Settings;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.TextView;
import android.R.layout;
import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.spark.submitbutton.SubmitButton;
import com.testobject.httprequest.respDeviceCadastro.DeviceCadastro;
import com.thanosfisherman.wifiutils.WifiConnectorBuilder;
import com.thanosfisherman.wifiutils.WifiUtils;

import java.io.InputStream;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.ExecutionException;

public class MainActivity extends AppCompatActivity {

    static String ipWoxintonn = "http://192.168.4.1/?";
    static String urlApi = "http://nexsolar.sytes.net/ceb/api/estacao/usuario/";
    static String api = "http://nexsolar.sytes.net/ceb/api/estacao/usuario/";
    static String responseCode = "";
    static String endpoint = "";
    private TextView TxtPassword;
    private TextInputEditText TxtSSID;
    private AutoCompleteTextView TxtTipo;
    private TimePickerDialog picker;
    private TextView responseStatusField;
    private SubmitButton get;
    private String resp;
    private ProgressDialog dialog;
    private Integer i;
    private String userName;
    private Integer userId;
    private String cookieName;
    private String cookieValue;
    private DeviceCadastro[] deviceList;
    private AlertDialog.Builder errorDialog;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_installer);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        getBundle();

        declaration();

        generatList();

        TxtTipo.setOnFocusChangeListener(new View.OnFocusChangeListener() {
            @Override
            public void onFocusChange(View view, boolean b) {
                TxtTipo.showDropDown();
            }
        });

        TxtTipo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                TxtTipo.showDropDown();
            }
        });

        if (savedInstanceState == null) {
            get.setOnClickListener(view -> {
                responseStatusField.setText(null);
                resp ="";
                Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("GMT"),
                        Locale.getDefault());
                Date currentLocalTime = calendar.getTime();

                DateFormat date = new SimpleDateFormat("ZZZZZ",Locale.getDefault());
                startDialog();
                Thread thread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        endpoint = ipWoxintonn +
                                "ssid=" + TxtSSID.getText().toString() +
                                "&password=" + TxtPassword.getText().toString() +
                                "&type=" + getType(TxtTipo.getText().toString()) +
                                "&fuso=" + date.format(currentLocalTime);
                        resp = getResponse(endpoint);
                        Log.v("endpoint", endpoint);
                        Log.v("resp", resp);
                        resp = getResponse(ipWoxintonn + "hskvsckv=true");
                        Log.v("resp dly", resp);
                    }
                });
                thread.start();
            });
        }
    }

    private void startDialog(){
        dialog.setTitle("Conectando");
        dialog.setMessage("Calma lá que já conecta...");
        dialog.setCanceledOnTouchOutside(false);
        dialog.setMax(100);
        dialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        dialog.show();

        Timer timer = new Timer();
        i = 0;
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                i++;

                resp = getResponse(ipWoxintonn + "free=true");
                Log.v("eita->>>>", resp);

                if("CONECTADOO!".equals(resp)) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            responseStatusField.setText("Conexão Realizada com Sucesso! xD");
                        }
                    });
                    dialog.dismiss();
                    timer.cancel();
                    timer.purge();
                }
                else if( i > 60){
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            responseStatusField.setText("Falha ao conectar na rede :'(");
                        }
                    });
                    dialog.dismiss();
                    timer.cancel();
                    timer.purge();
                }

            }
        }, 0, 200);
    }

    public String getResponse(String ip){
        String resposta = "errou";
        try {
            final java.net.URL url = new URL(ip);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            resposta = new String(ByteStreams.toByteArray(stream));
            Log.v("uehuehuheue", resposta);
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }
        return resposta;
    }

    public DeviceCadastro[] getDeviceCadastro(){
        try {
            final java.net.URL url = new URL(urlApi);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            String cookie = cookieName + "=" + cookieValue +"; domain=192.168.0.30";
            connection.setRequestProperty("Cookie", cookie);
            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Log.v("oloco", oloco);
            DeviceCadastro[] msg = new Gson().fromJson(oloco, DeviceCadastro[].class);
            return msg;
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }

        return null;
    }

    public void generatList(){
        startDialog("Buscando", "Buscando lista de dispositivos");
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {

                    deviceList = getDeviceCadastro();

                    MainActivity.this.runOnUiThread(new Runnable() {
                        public void run() {
                            startErrorDialog("Realizar conexão:", "Conecte-se a rede da estação");
                        }
                    });

                    ArrayAdapter<String> adapter = new ArrayAdapter<String>(MainActivity.this, layout.simple_list_item_1, deviceNameList());

                    MainActivity.this.runOnUiThread(new Runnable() {
                        public void run() {
                            TxtTipo.setAdapter(adapter);
                        }
                    });
                    dialog.dismiss();

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                    dialog.dismiss();
                }
            }
        });
        thread.start();
    }

    public void startDialog(String title, String msg){
        dialog = new ProgressDialog(MainActivity.this);
        dialog.setIndeterminate(true);
        dialog.setTitle(title);
        dialog.setMessage(msg);
        dialog.setCanceledOnTouchOutside(false);
        dialog.setMax(100);
        dialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        dialog.show();
    }

    public String [] deviceNameList(){
        String[] resp = new String[deviceList.length];
        for (int i = 0; i< resp.length; i++) {
            resp[i] = deviceList[i].name();
            Log.v(Integer.toString(i), resp[i]);
        }
        return resp;
    }

    public String getType(String name){
        for(DeviceCadastro device: deviceList){
            if(device.name().equals(name)) return device.getIdEstacao();
        }
        return "-1";
    }

    public void getBundle(){
        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        if (bundle != null){
            userName = getIntent().getStringExtra("userName");
            userId = getIntent().getIntExtra("userId",0);
            urlApi = api + userId + "/cadastrar";
            cookieName = (String) getIntent().getSerializableExtra("cookieName");
            cookieValue = (String) getIntent().getSerializableExtra("cookieValue");
        }
    }

    public void declaration(){
        TxtSSID =  findViewById(R.id.txt_ssid);
        TxtPassword = (TextView) findViewById(R.id.txt_password);
        TxtTipo = findViewById(R.id.txt_type);
        get = findViewById(R.id.button);
        responseStatusField = (TextView) findViewById(R.id.response_status);
        dialog = new ProgressDialog(MainActivity.this);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            TxtTipo.setShowSoftInputOnFocus(false);
        } else {
            try {
                final Method method = AutoCompleteTextView.class.getMethod(
                        "setShowSoftInputOnFocus"
                        , boolean.class);
                method.setAccessible(true);
                method.invoke(TxtTipo, false);
            } catch (Exception e) {
                // ignore
            }
        }
    }

    public void startErrorDialog(String title, String msg){
        errorDialog= new AlertDialog.Builder(this);
        errorDialog.setTitle(title);
        errorDialog.setMessage(msg);
        if(title.equals("Erro de rede:")) errorDialog.setPositiveButton("OK", (dialog, id) -> startActivity(new Intent(Settings.ACTION_WIFI_SETTINGS)));
        else errorDialog.setPositiveButton("OK", null);
        AlertDialog alerta = errorDialog.create();
        alerta.show();
    }

}
