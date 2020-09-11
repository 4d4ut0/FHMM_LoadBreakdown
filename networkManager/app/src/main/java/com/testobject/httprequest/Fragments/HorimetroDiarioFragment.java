package com.testobject.httprequest.Fragments;

import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.TextView;

import androidx.fragment.app.DialogFragment;
import androidx.fragment.app.Fragment;

import com.google.common.io.ByteStreams;
import com.google.gson.Gson;
import com.jjoe64.graphview.DefaultLabelFormatter;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.testobject.httprequest.DatePickerFragment;
import com.testobject.httprequest.R;
import com.testobject.httprequest.respConsumo.Consumo;
import com.testobject.httprequest.respConsumo.respConsumo;
import com.testobject.httprequest.respDevice.Device;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

public class HorimetroDiarioFragment extends Fragment {
    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";
    private static final String ARG_PARAM3 = "param3";
    // TODO: Rename and change types of parameters
    private String userName;
    private String userId;
    private String estacaoId;
    private String urlInicial = "http://nexsolar.sytes.net/ceb/api/consumo/";
    private String api = "/diario/";
    private String urlDevice = "http://nexsolar.sytes.net/ceb/api/estacao/usuario/";
    private Device[] deviceList;
    private ArrayList<Consumo> respsConsumos;
    private ArrayList<Date> x;
    private ArrayList<Float> y;
    private ProgressDialog progressDialog;
    private View rootView;
    private GraphView graph;
    private TextView txtData;
    private Button btnGenerate;
    public HorimetroDiarioFragment() {
        // Required empty public constructor
    }
    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment HomeFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static DiarioFragment newInstance(String param1, String param2, String param3) {
        DiarioFragment fragment = new DiarioFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        args.putString(ARG_PARAM3, param3);
        fragment.setArguments(args);
        return fragment;
    }
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (getArguments() != null) {
            userName = getArguments().getString(ARG_PARAM1);
            userId = getArguments().getString(ARG_PARAM2);
            estacaoId = getArguments().getString(ARG_PARAM3);
        }

    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        declaration(inflater, container);

        InputMethodManager in = (InputMethodManager) getActivity().getSystemService(Context.INPUT_METHOD_SERVICE);

        txtData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DialogFragment dialogfragment = new DatePickerFragment("diario");
                dialogfragment.setCancelable(false);
                dialogfragment.show(getFragmentManager(), "Theme 3");
            }
        });

        btnGenerate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                generatGraph();
            }
        });

        return rootView;
    }

    public ArrayList<Consumo> getConsumo(String estacaoId, String data){
        try {
            final java.net.URL url = new URL(urlInicial + estacaoId + api + data);
            final HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.connect();

            final InputStream stream = connection.getInputStream();
            String oloco = new String(ByteStreams.toByteArray(stream));
            Log.v("oloco", oloco);
            respConsumo msg = new Gson().fromJson(oloco, respConsumo.class);
            if (msg == null) return null;
            else return sortByDate(msg.getConsumos());
        } catch (Exception e){
            Log.e("Your tag", "Error", e);
        }
        return null;
    }

    public ArrayList<Date> findDataConsumo (){
        ArrayList<Date> resp = new ArrayList<>();
        for (Consumo consumo: respsConsumos) {
            resp.add(convertStringToDate(consumo.getDataTimeInsere()));
        }

        return resp;
    }

    public ArrayList<Float> findPotenciaConsumo (){
        ArrayList<Float> resp = new ArrayList<>();
        for (Consumo consumo: respsConsumos)
            resp.add(consumo.getPotencia())  ;

        return resp;
    }

    public void startDialog(String title, String msg){
        progressDialog = new ProgressDialog(getContext());
        progressDialog.setIndeterminate(true);
        progressDialog.setTitle(title);
        progressDialog.setMessage(msg);
        progressDialog.setCanceledOnTouchOutside(false);
        progressDialog.setMax(100);
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
    }

    public void generatGraph(){
        startDialog("Buscando dados de consumo", "Tiruriruriruruuuu, rururu, rurururuuuuu");
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try  {


                } catch (Exception e) {
                    Log.e("iririr", "Erro no parsing do JSON", e);
                }
            }
        });
        thread.start();
    }

    public Date convertStringToDate(String dtStart){
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
        try {
            Date date = format.parse(dtStart);
            return date;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return  null;
    }

    public ArrayList<Consumo> sortByDate(ArrayList<Consumo> consumos){
        Consumo aux;
        for(int i = 0; i < consumos.size(); i++)
            for(int j = 0; j < consumos.size(); j++){
                if(consumos.get(i).compareTo(consumos.get(j)) < 0){
                    aux = consumos.get(j);
                    consumos.set(j, consumos.get(i));
                    consumos.set(i, aux);
                }
            }
        return consumos;
    }

    public String findIdbyName(String name){
        String last = "-1";
        for(Device device: deviceList){
            if(device.getTipo().equals(name)) if(device.getIdEstacao().toString().equals(estacaoId))last = device.getIdEstacao().toString();
        }
        return last;
    }

    public void declaration(LayoutInflater inflater, ViewGroup container){
        rootView = inflater.inflate(R.layout.fragment_diario_horimetro, container, false);
        graph = rootView.findViewById(R.id.graph);
        txtData = rootView.findViewById(R.id.txt_data);
        btnGenerate = rootView.findViewById(R.id.button_generate);

        final Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int day = calendar.get(Calendar.DAY_OF_MONTH);
        //txtData.setText(day+"/"+month+"/"+year);
        txtData.setText("18/04/2011");
        
    }

}
