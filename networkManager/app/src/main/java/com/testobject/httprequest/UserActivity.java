package com.testobject.httprequest;

import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.testobject.httprequest.respJsonLogin.respJsonLogin;

public class UserActivity extends AppCompatActivity {
    private static final int REQUEST_SIGNUP = 0;
    private static final String REQUEST_ESTACAO = "ESTACAO";
    private static final String REQUEST_HORIMETRO = "HORIMETRO";
    private respJsonLogin respJson;
    private CardView cv_estacoes;
    private CardView cv_horimetross;
    private CardView cv_perfil;
    private CardView cv_conectar;
    private LinearLayout ll_watts_dia;
    private LinearLayout ll_co2_dia;

    private Integer id;
    private String nome;
    private String cpf;
    private String status;
    private Integer status_color;
    private String tipo;
    private String descricao;

    private TextView txt_nome;
    private TextView txt_cpf;
    private TextView txt_status;
    private TextView txt_tipo;
    private TextView txt_descricao;
    private Dialog dl_perfil;

    private ImageView img;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        if (bundle != null){
            respJson = (respJsonLogin) getIntent().getSerializableExtra("json");
            id = respJson.getResult().getIdUsuario();
            nome = respJson.getResult().getNome();
            cpf = respJson.getResult().getCpf();
            status = (respJson.getResult().getAtivo()) ?  "Ativo" : "Inativo";
            status_color = (respJson.getResult().getAtivo()) ?  getResources().getColor(R.color.green) : getResources().getColor(R.color.pink);
            tipo = respJson.getResult().getPerfil().getNome();
            descricao = respJson.getResult().getPerfil().getDescricao();

        }

        declaration();
        declaration_dl();

        //btnMonitor = findViewById(R.id.buttonMonitor);
        //btnNewDV = findViewById(R.id.buttonNewDV);

//        btnMonitor.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                sendMonitoramento(respJson.getResult().getIdUsuario(),respJson.getResult().getNome());
//            }
//        });

        cv_estacoes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendUserId(REQUEST_ESTACAO);
            }
        });
        cv_horimetross.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendUserId(REQUEST_HORIMETRO);
            }
        });
        cv_perfil.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fill_dl();
                dl_perfil.show();
            }
        });
        cv_conectar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendNewDV();
            }
        });
        ll_watts_dia.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });
        ll_co2_dia.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

            }
        });


    }

    public void sendNewDV(){
        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("userName", nome);
        bundle.putInt("userId", id);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);
    }

    public void sendUserId(String request){
        Intent intent = new Intent(getApplicationContext(), DeviceListActivity.class);
        Bundle bundle = new Bundle();
        bundle.putInt("userId", id);
        intent.putExtras(bundle);
        intent.setAction(request);
        startActivityForResult(intent,0);
    }

    public void sendMonitoramento(Integer id, String name){
        Intent intent = new Intent(getApplicationContext(), UserConsumoActivity.class);
        Bundle bundle = new Bundle();
        bundle.putString("userName", name);
        bundle.putInt("userId", id);
        intent.putExtras(bundle);
        startActivityForResult(intent, REQUEST_SIGNUP);
    }

    public void declaration(){
        cv_estacoes = findViewById(R.id.go_estacoes);
        cv_horimetross = findViewById(R.id.go_horimetros);
        cv_perfil = findViewById(R.id.go_perfil);
        cv_conectar = findViewById(R.id.go_config);
        ll_watts_dia = findViewById(R.id.go_watts_dia);
        ll_co2_dia = findViewById(R.id.go_co2_dia);
    }

    private void declaration_dl(){
        dl_perfil = new Dialog(UserActivity.this);
        dl_perfil.setContentView(R.layout.layout_perfil);

        txt_nome = dl_perfil.findViewById(R.id.txt_name);
        txt_cpf = dl_perfil.findViewById(R.id.txt_cpf);
        txt_status = dl_perfil.findViewById(R.id.txt_status);
        txt_tipo = dl_perfil.findViewById(R.id.txt_tipo);
        txt_descricao = dl_perfil.findViewById(R.id.txt_descricao);
    }

    private void fill_dl(){
        txt_nome.setText(nome);
        txt_cpf.setText(cpf);
        txt_status.setText(status);
        txt_status.setBackgroundColor(status_color);
        txt_tipo.setText(tipo);
        txt_descricao.setText(descricao);
    }

}
