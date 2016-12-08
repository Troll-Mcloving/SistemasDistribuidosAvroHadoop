/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package avropesquisadores;

import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.avro.file.DataFileReader;
import org.apache.avro.io.DatumReader;
import org.apache.avro.specific.SpecificDatumReader;

/**
 *
 * @author Leonardo
 */
public class AvroPesquisadores {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        try {
            // Deserialize Users from disk
            File file = new File("Pesquisador.avro");
            DatumReader<Pesquisador> userDatumReader = new SpecificDatumReader<Pesquisador>(Pesquisador.class);
            DataFileReader<Pesquisador> dataFileReader = new DataFileReader<Pesquisador>(file, userDatumReader);
            Pesquisador pesquisador = null;
            while(dataFileReader.hasNext()) {
                pesquisador = dataFileReader.next(pesquisador);
                System.out.println(pesquisador);
            }
        } catch(IOException ex) {
            Logger.getLogger(AvroPesquisadores.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

}
