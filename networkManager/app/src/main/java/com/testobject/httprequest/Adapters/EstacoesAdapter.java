package com.testobject.httprequest.Adapters;

import android.content.Context;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.testobject.httprequest.R;
import com.testobject.httprequest.UserConsumoActivity;
import com.testobject.httprequest.respDevice.Device;

import java.util.List;

import static androidx.core.app.ActivityCompat.startActivityForResult;

public class EstacoesAdapter extends RecyclerView.Adapter<EstacoesAdapter.EstacoesViewHolder> {
    @NonNull


    private Context mCtx;
    private List<Device> estacoesList;
    private String id;

    public EstacoesAdapter(Context mCtx, List<Device> estacoesList, String id) {
        this.mCtx = mCtx;
        this.estacoesList = estacoesList;
        this.id = id;
    }

    @Override
    public EstacoesViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(mCtx);
        View view = inflater.inflate(R.layout.layout_estacoes, null);
        return new EstacoesViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull EstacoesViewHolder holder, int position) {
        Device estacao = estacoesList.get(position);

        //holder.id_user = Integer.toString(estacao.getIdUsuario());
        holder.id_user = id;
        holder.id_estacao = Integer.toString(estacao.getIdEstacao());
        holder.name_user = estacao.getNomeUsuario();

        holder.txt_nome.setText(estacao.getApelido());
        holder.txt_mac.setText(estacao.getIdHardware());
        holder.txt_origem.setText((estacao.getVirtual())?  "Virtual" : "Real");
        holder.txt_tipo.setText(estacao.getTipo());

        holder.img_icon.setBackground((estacao.getOnline())? mCtx.getDrawable(R.drawable.cercleshape_on) :  mCtx.getDrawable(R.drawable.cercleshape_off));
        holder.txt_origem.setBackgroundColor((estacao.getVirtual())?   mCtx.getColor(R.color.colorPrimary) : mCtx.getColor(R.color.blue));

        holder.img_icon.setImageDrawable(mCtx.getResources().getDrawable(getIcon(estacao.getTipo())));
    }

    @Override
    public int getItemCount() {
        return estacoesList.size();
    }

    public class EstacoesViewHolder extends RecyclerView.ViewHolder{
        TextView txt_nome, txt_mac, txt_origem, txt_tipo;
        ImageView img_icon;
        RelativeLayout rl_card;
        String id_user, id_estacao, name_user;

        public EstacoesViewHolder(@NonNull View itemView) {
            super(itemView);

            txt_nome = itemView.findViewById(R.id.txt_nome);
            txt_mac = itemView.findViewById(R.id.txt_mac);
            txt_origem = itemView.findViewById(R.id.txt_origem);
            txt_tipo = itemView.findViewById(R.id.txt_tipo);
            img_icon = itemView.findViewById(R.id.img_icon);
            rl_card = itemView.findViewById(R.id.rl_card);

            rl_card.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(mCtx, UserConsumoActivity.class);
                    Bundle bundle = new Bundle();
                    bundle.putString("userName", name_user);
                    bundle.putString("userId", id_user);
                    bundle.putString("estacaoId", id_estacao);
                    bundle.putString("estacaoName", txt_nome.getText().toString());
                    intent.putExtras(bundle);
                    mCtx.startActivity(intent);
                }
            });
        }
    }

    private Integer getIcon(String tipo){
        if(tipo.toLowerCase().equals("geladeira"))
            return R.drawable.ic_type_smart_refrigerator;
        else if(tipo.toLowerCase().equals("pc"))
            return R.drawable.ic_type_laptop;
        else if(tipo.toLowerCase().equals("micro-ondas"))
            return R.drawable.ic_type_microwave;
        else if(tipo.toLowerCase().equals("batedeira"))
            return R.drawable.ic_type_mixer_blender;
        else if(tipo.toLowerCase().equals("tv"))
            return R.drawable.ic_type_smart_tv;
        else if(tipo.toLowerCase().equals("maquina de lavar"))
            return R.drawable.ic_type_washing_machine;
        else if(tipo.toLowerCase().equals("aquecedor de água"))
            return R.drawable.ic_type_water_heater;
        else if(tipo.toLowerCase().equals("mains"))
            return R.drawable.ic_type_main;
        else
            return R.drawable.ic_type_plug;
    }
}
