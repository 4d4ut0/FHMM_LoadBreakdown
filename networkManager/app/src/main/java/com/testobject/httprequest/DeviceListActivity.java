package com.testobject.httprequest;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;

import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.testobject.httprequest.Adapters.EstacoesAdapter;
import com.testobject.httprequest.Adapters.HorimetrosAdapter;
import com.testobject.httprequest.respDevice.Device;
import com.testobject.httprequest.respHorimetro.Horimetro;
import com.testobject.httprequest.respJsonLogin.respJsonLogin;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DeviceListActivity extends AppCompatActivity {
    private static final int REQUEST_SIGNUP = 0;
    private static final String REQUEST_ESTACAO = "ESTACAO";
    private static final String REQUEST_HORIMETRO = "HORIMETRO";
    private List<Device> estacaoList;
    private List<Horimetro> horimetroList;
    private RecyclerView recyclerView;
    private String urlEstacao = "http://nexsolar.sytes.net/chesp/api/estacao/usuario/";
    private String urlHorimetro = "http://nexsolar.sytes.net/chesp/api/horimetro/usuario/";
    private String id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_estacoes_list);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        String request = intent.getAction();
        if (bundle != null){
            //id = Integer.toString(bundle.getInt("userId"));
            id = "13";
        }

        if(request == REQUEST_ESTACAO){
            declaration_dv();
        }
        else if(request == REQUEST_HORIMETRO){
            declaration_hm();
        }

    }


    public List<Device> getDevices(){
        try {
            final java.net.URL url = new URL(urlEstacao + id);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Device[] msg = new Gson().fromJson(oloco, Device[].class);
            return new ArrayList<>(Arrays.asList(msg));
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }
        return null;
    }

    public List<Horimetro> getHorimeters(){
        try {
            final java.net.URL url = new URL(urlHorimetro + id);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Horimetro[] msg = new Gson().fromJson(oloco, Horimetro[].class);
            return new ArrayList<>(Arrays.asList(msg));
        } catch (Exception e) {
            Log.e("Your tag", "Error", e);
        }
        return null;
    }

    private void declaration_dv(){
        recyclerView = findViewById(R.id.rv_dv);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {
                    estacaoList = getDevices();
                    EstacoesAdapter adapter = new EstacoesAdapter(DeviceListActivity.this, estacaoList, id);

                    DeviceListActivity.this.runOnUiThread(new Runnable() {
                        public void run() {
                            if(estacaoList != null) {
                                recyclerView.setAdapter(adapter);
                            }
                        }
                    });

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }

    private void declaration_hm(){
        recyclerView = findViewById(R.id.rv_dv);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {
                    horimetroList = getHorimeters();
                    HorimetrosAdapter adapter = new HorimetrosAdapter(DeviceListActivity.this, horimetroList);

                    DeviceListActivity.this.runOnUiThread(new Runnable() {
                        public void run() {
                            if(horimetroList != null) {
                                recyclerView.setAdapter(adapter);
                            }
                        }
                    });

                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }
}
