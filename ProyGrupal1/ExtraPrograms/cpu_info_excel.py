import os
import sys
from pathlib import Path

# Añadir el directorio actual al path para imports relativos
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(current_dir))

from table_control import DataType, TableControl

class CPUInfoExcel:
    """Clase para manejar la lectura y escritura de señales del CPU en Excel"""
    
    def __init__(self):
        self.table = TableControl()
        # Diccionario para caché de memoria - más eficiente que métodos individuales
        self._memory_cache = {}
        self._memory_base_row = 1  # Fila inicial para bloques de memoria
        self._memory_base_col = 29  # Columna para bloques de memoria
    
    #=================================================================================
    # Señales del Decode
    #=================================================================================
    def write_pc_prime(self, value):
        """Escribe el valor de PC' en la cola de acciones"""
        self.table.write(1, 2, value)

    def read_pc_prime(self):
        """
        Lee inmediatamente el valor de PC' 
        
        Returns:
            Tuple[DataType, Any]: Tupla con el tipo de dato y el valor de PC'
        """
        return self.table.read_immediate(1, 2)

    def write_pcf(self, value):
        """Escribe el valor de PCF en la cola de acciones"""
        self.table.write(2, 2, value)

    def read_pcf(self):
        """
        Lee inmediatamente el valor de PCF
        
        Returns:
            Tuple[DataType, Any]: Tupla con el tipo de dato y el valor de PCF
        """
        return self.table.read_immediate(2, 2)

    def write_pcplus8f(self, value):
        """Escribe el valor de PCPlus8F en la cola de acciones"""
        self.table.write(3, 2, value)

    def read_pcplus8f(self):
        """
        Lee inmediatamente el valor de PCPlus8F
        
        Returns:
            Tuple[DataType, Any]: Tupla con el tipo de dato y el valor de PCPlus8F
        """
        return self.table.read_immediate(3, 2)

    def write_instrf(self, value):
        """Escribe el valor de InstrF en la cola de acciones"""
        self.table.write(4, 2, value)

    def read_instrf(self):
        return self.table.read_immediate(4, 2)
        
    #=================================================================================
    # Señales del Fetch
    #=================================================================================
    def write_instrd(self, value):
        self.table.write(1, 5, value)
    
    def read_instrd(self):
        return self.table.read_immediate(1, 5)
    
    def write_pcf_d(self, value):
        self.table.write(2, 5, value)
    
    def read_pcf_d(self):
        return self.table.read_immediate(2, 5)
    
    def write_55_52(self, value):
        self.table.write(3, 5, value)
    
    def read_55_52(self):
        return self.table.read_immediate(3, 5)
    
    def write_63_56(self, value):
        self.table.write(4, 5, value)
    
    def read_63_56(self):
        return self.table.read_immediate(4, 5)
    
    def write_47_44(self, value):
        self.table.write(5, 5, value)
    
    def read_47_44(self):
        return self.table.read_immediate(5, 5)
    
    def write_43_40(self, value):
        self.table.write(6, 5, value)
    
    def read_43_40(self):
        return self.table.read_immediate(6, 5)
    
    def write_39_8(self, value):
        self.table.write(7, 5, value)
    
    def read_39_8(self):
        return self.table.read_immediate(7, 5)
    
    def write_51_48(self, value):
        self.table.write(8, 5, value)
    
    def read_51_48(self):
        return self.table.read_immediate(8, 5)
    
    def write_memwritep(self, value):
        self.table.write(9, 5, value)
    
    def read_memwritep(self):
        return self.table.read_immediate(9, 5)
    
    def write_memwritev(self, value):
        self.table.write(10, 5, value)
    
    def read_memwritev(self):
        return self.table.read_immediate(10, 5)
    
    def write_registerina(self, value):
        self.table.write(11, 5, value)
    
    def read_registerina(self):
        return self.table.read_immediate(11, 5)
    
    def write_registerinb(self, value):
        self.table.write(12, 5, value)
    
    def read_registerinb(self):
        return self.table.read_immediate(12, 5)
    
    def write_immediateop(self, value):
        self.table.write(13, 5, value)
    
    def read_immediateop(self):
        return self.table.read_immediate(13, 5)
    
    def write_branche(self, value):
        self.table.write(14, 5, value)
    
    def read_branche(self):
        return self.table.read_immediate(14, 5)
    
    def write_logoutd(self, value):
        self.table.write(15, 5, value)
    
    def read_logoutd(self):
        return self.table.read_immediate(15, 5)
    
    def write_comsd(self, value):
        self.table.write(16, 5, value)
    
    def read_comsd(self):
        return self.table.read_immediate(16, 5)
    
    def write_printend(self, value):
        self.table.write(17, 5, value)
    
    def read_printend(self):
        return self.table.read_immediate(17, 5)
    
    def write_regwritesd(self, value):
        self.table.write(18, 5, value)
    
    def read_regwritesd(self):
        return self.table.read_immediate(18, 5)
    
    def write_regwriterd(self, value):
        self.table.write(19, 5, value)
    
    def read_regwriterd(self):
        return self.table.read_immediate(19, 5)
    
    def write_memopd(self, value):
        self.table.write(20, 5, value)
    
    def read_memopd(self):
        return self.table.read_immediate(20, 5)
    
    def write_memwritegd(self, value):
        self.table.write(21, 5, value)
    
    def read_memwritegd(self):
        return self.table.read_immediate(21, 5)
    
    def write_memwritedd(self, value):
        self.table.write(22, 5, value)
    
    def read_memwritedd(self):
        return self.table.read_immediate(22, 5)
    
    def write_membyted(self, value):
        self.table.write(23, 5, value)
    
    def read_membyted(self):
        return self.table.read_immediate(23, 5)
    
    def write_pcsrcd(self, value):
        self.table.write(24, 5, value)
    
    def read_pcsrcd(self):
        return self.table.read_immediate(24, 5)
    
    def write_flagsupdd(self, value):
        self.table.write(25, 5, value)
    
    def read_flagsupdd(self):
        return self.table.read_immediate(25, 5)
    
    def write_alusrcd(self, value):
        self.table.write(26, 5, value)
    
    def read_alusrcd(self):
        return self.table.read_immediate(26, 5)
    
    def write_branchopd(self, value):
        self.table.write(27, 5, value)
    
    def read_branchopd(self):
        return self.table.read_immediate(27, 5)
    
    def write_rdr1_a(self, value):
        self.table.write(28, 5, value)
    
    def read_rdr1_a(self):
        return self.table.read_immediate(28, 5)
    
    def write_rdr2_a(self, value):
        self.table.write(29, 5, value)
    
    def read_rdr2_a(self):
        return self.table.read_immediate(29, 5)
    
    def write_rdw1_a(self, value):
        self.table.write(30, 5, value)
    
    def read_rdw1_a(self):
        return self.table.read_immediate(30, 5)
    
    def write_rdw2_a(self, value):
        self.table.write(31, 5, value)
    
    def read_rdw2_a(self):
        return self.table.read_immediate(31, 5)
    
    def write_kd_a(self, value):
        self.table.write(32, 5, value)
    
    def read_kd_a(self):
        return self.table.read_immediate(32, 5)
    
    def write_rd_a(self, value):
        self.table.write(33, 5, value)
    
    def read_rd_a(self):
        return self.table.read_immediate(33, 5)
    
    def write_srcad_0(self, value):
        self.table.write(34, 5, value)
    
    def read_srcad_0(self):
        return self.table.read_immediate(34, 5)
    
    def write_srcad(self, value):
        self.table.write(35, 5, value)
    
    def read_srcad(self):
        return self.table.read_immediate(35, 5)
    
    def write_rd_speciald(self, value):
        self.table.write(36, 5, value)
    
    def read_rd_speciald(self):
        return self.table.read_immediate(36, 5)
    
    def write_srcbd(self, value):
        self.table.write(37, 5, value)
    
    def read_srcbd(self):
        return self.table.read_immediate(37, 5)
    #=================================================================================
    # Señales del Execute
    #=================================================================================
    def write_regwritese(self, value):
        self.table.write(1, 8, value)
    
    def read_regwritese(self):
        return self.table.read_immediate(1, 8)
    
    def write_regwritere(self, value):
        self.table.write(2, 8, value)
    
    def read_regwritere(self):
        return self.table.read_immediate(2, 8)
    
    def write_memope(self, value):
        self.table.write(3, 8, value)
    
    def read_memope(self):
        return self.table.read_immediate(3, 8)
    
    def write_memwritege(self, value):
        self.table.write(4, 8, value)
    
    def read_memwritege(self):
        return self.table.read_immediate(4, 8)
    
    def write_memwritede(self, value):
        self.table.write(5, 8, value)
    
    def read_memwritede(self):
        return self.table.read_immediate(5, 8)
    
    def write_membytee(self, value):
        self.table.write(6, 8, value)
    
    def read_membytee(self):
        return self.table.read_immediate(6, 8)
    
    def write_pcsrce(self, value):
        self.table.write(7, 8, value)
    
    def read_pcsrce(self):
        return self.table.read_immediate(7, 8)
    
    def write_flagsupde(self, value):
        self.table.write(8, 8, value)
    
    def read_flagsupde(self):
        return self.table.read_immediate(8, 8)
    
    def write_alusrce(self, value):
        self.table.write(9, 8, value)
    
    def read_alusrce(self):
        return self.table.read_immediate(9, 8)
    
    def write_branchope(self, value):
        self.table.write(10, 8, value)
    
    def read_branchope(self):
        return self.table.read_immediate(10, 8)
    
    def write_printene(self, value):
        self.table.write(11, 8, value)
    
    def read_printene(self):
        return self.table.read_immediate(11, 8)
    
    def write_comse(self, value):
        self.table.write(12, 8, value)
    
    def read_comse(self):
        return self.table.read_immediate(12, 8)
    
    def write_logoute(self, value):
        self.table.write(13, 8, value)
    
    def read_logoute(self):
        return self.table.read_immediate(13, 8)
    
    def write_branchope_2(self, value):
        self.table.write(14, 8, value)
    
    def read_branchope_2(self):
        return self.table.read_immediate(14, 8)
    
    def write_flagse(self, value):
        self.table.write(15, 8, value)
    
    def read_flagse(self):
        return self.table.read_immediate(15, 8)
    
    def write_srcae(self, value):
        self.table.write(16, 8, value)
    
    def read_srcae(self):
        return self.table.read_immediate(16, 8)
    
    def write_rd_speciale(self, value):
        self.table.write(17, 8, value)
    
    def read_rd_speciale(self):
        return self.table.read_immediate(17, 8)
    
    def write_srcbe(self, value):
        self.table.write(18, 8, value)
    
    def read_srcbe(self):
        return self.table.read_immediate(18, 8)
    
    def write_flags_prime(self, value):
        self.table.write(19, 8, value)
    
    def read_flags_prime(self):
        return self.table.read_immediate(19, 8)
    
    def write_aluflagout(self, value):
        self.table.write(20, 8, value)
    
    def read_aluflagout(self):
        return self.table.read_immediate(20, 8)
    
    def write_carryin(self, value):
        self.table.write(21, 8, value)
    
    def read_carryin(self):
        return self.table.read_immediate(21, 8)
    
    def write_condexe(self, value):
        self.table.write(22, 8, value)
    
    def read_condexe(self):
        return self.table.read_immediate(22, 8)
    
    def write_safeflagsout(self, value):
        self.table.write(23, 8, value)
    
    def read_safeflagsout(self):
        return self.table.read_immediate(23, 8)
    
    def write_logininblocke(self, value):
        self.table.write(24, 8, value)
    
    def read_logininblocke(self):
        return self.table.read_immediate(24, 8)
    
    def write_rde(self, value):
        self.table.write(25, 8, value)
    
    def read_rde(self):
        return self.table.read_immediate(25, 8)
    
    def write_aluresulte(self, value):
        self.table.write(26, 8, value)
    
    def read_aluresulte(self):
        return self.table.read_immediate(26, 8)
    
    def write_pcsrc_and_e(self, value):
        self.table.write(27, 8, value)
    
    def read_pcsrc_and_e(self):
        return self.table.read_immediate(27, 8)
    
    #=================================================================================
    # Señales del Memory
    #=================================================================================
    def write_regwritesm(self, value):
        self.table.write(1, 11, value)
    
    def read_regwritesm(self):
        return self.table.read_immediate(1, 11)
    
    def write_regwriterm(self, value):
        self.table.write(2, 11, value)
    
    def read_regwriterm(self):
        return self.table.read_immediate(2, 11)
    
    def write_memopm(self, value):
        self.table.write(3, 11, value)
    
    def read_memopm(self):
        return self.table.read_immediate(3, 11)
    
    def write_memwritegm(self, value):
        self.table.write(4, 11, value)
    
    def read_memwritegm(self):
        return self.table.read_immediate(4, 11)
    
    def write_memwritedm(self, value):
        self.table.write(5, 11, value)
    
    def read_memwritedm(self):
        return self.table.read_immediate(5, 11)
    
    def write_membytem(self, value):
        self.table.write(6, 11, value)
    
    def read_membytem(self):
        return self.table.read_immediate(6, 11)
    
    def write_pcsrcm(self, value):
        self.table.write(7, 11, value)
    
    def read_pcsrcm(self):
        return self.table.read_immediate(7, 11)
    
    def write_printenm(self, value):
        self.table.write(8, 11, value)
    
    def read_printenm(self):
        return self.table.read_immediate(8, 11)
    
    def write_aluoutm(self, value):
        self.table.write(9, 11, value)
    
    def read_aluoutm(self):
        return self.table.read_immediate(9, 11)
    
    def write_rd_specialm(self, value):
        self.table.write(10, 11, value)
    
    def read_rd_specialm(self):
        return self.table.read_immediate(10, 11)
    
    def write_rdm(self, value):
        self.table.write(11, 11, value)
    
    def read_rdm(self):
        return self.table.read_immediate(11, 11)
    
    def write_rd_specialm_b(self, value):
        self.table.write(12, 11, value)
    
    def read_rd_specialm_b(self):
        return self.table.read_immediate(12, 11)
    
    def write_rd_specialm_c(self, value):
        self.table.write(13, 11, value)
    
    def read_rd_specialm_c(self):
        return self.table.read_immediate(13, 11)
    
    def write_rd_specialm_d(self, value):
        self.table.write(14, 11, value)
    
    def read_rd_specialm_d(self):
        return self.table.read_immediate(14, 11)
    
    def write_rd_specialm_e(self, value):
        self.table.write(15, 11, value)
    
    def read_rd_specialm_e(self):
        return self.table.read_immediate(15, 11)
    
    def write_rd_g_a(self, value):
        self.table.write(16, 11, value)
    
    def read_rd_g_a(self):
        return self.table.read_immediate(16, 11)
    
    def write_rd_d_a(self, value):
        self.table.write(17, 11, value)
    
    def read_rd_d_a(self):
        return self.table.read_immediate(17, 11)
    
    def write_aluoutm_o(self, value):
        self.table.write(18, 11, value)
    
    def read_aluoutm_o(self):
        return self.table.read_immediate(18, 11)
    
    #=================================================================================
    # Señales del WriteBack
    #=================================================================================
    def write_regwritesm_wb(self, value):
        self.table.write(1, 14, value)
    
    def read_regwritesm_wb(self):
        return self.table.read_immediate(1, 14)
    
    def write_regwriterm_wb(self, value):
        self.table.write(2, 14, value)
    
    def read_regwriterm_wb(self):
        return self.table.read_immediate(2, 14)
    
    def write_pcsrcm_wb(self, value):
        self.table.write(3, 14, value)
    
    def read_pcsrcm_wb(self):
        return self.table.read_immediate(3, 14)
    
    def write_membytem_wb(self, value):
        self.table.write(4, 14, value)
    
    def read_membytem_wb(self):
        return self.table.read_immediate(4, 14)
    
    def write_printenm_wb(self, value):
        self.table.write(5, 14, value)
    
    def read_printenm_wb(self):
        return self.table.read_immediate(5, 14)
    
    def write_aluoutw(self, value):
        self.table.write(6, 14, value)
    
    def read_aluoutw(self):
        return self.table.read_immediate(6, 14)
    
    def write_aluoutw_b(self, value):
        self.table.write(7, 14, value)
    
    def read_aluoutw_b(self):
        return self.table.read_immediate(7, 14)
    
    def write_aluoutw_c(self, value):
        self.table.write(8, 14, value)
    
    def read_aluoutw_c(self):
        return self.table.read_immediate(8, 14)
    
    def write_int_pl(self, value):
        self.table.write(9, 14, value)
    
    def read_int_pl(self):
        return self.table.read_immediate(9, 14)
    
    def write_acii_pl(self, value):
        self.table.write(10, 14, value)
    
    def read_acii_pl(self):
        return self.table.read_immediate(10, 14)
    
    def write_b_pl(self, value):
        self.table.write(11, 14, value)
    
    def read_b_pl(self):
        return self.table.read_immediate(11, 14)
    
    def write_rdw(self, value):
        self.table.write(12, 14, value)
    
    def read_rdw(self):
        return self.table.read_immediate(12, 14)
    
    #=================================================================================
    # Valores actuales de registros generales
    #=================================================================================
    def write_r0(self, value):
        self.table.write(1, 17, 0x00000000)
    
    def read_r0(self):
        return self.table.read_immediate(1, 17)
    
    def write_r1(self, value):
        self.table.write(2, 17, value)
    
    def read_r1(self):
        return self.table.read_immediate(2, 17)
    
    def write_r2(self, value):
        self.table.write(3, 17, value)
    
    def read_r2(self):
        return self.table.read_immediate(3, 17)
    
    def write_r3(self, value):
        self.table.write(4, 17, value)
    
    def read_r3(self):
        return self.table.read_immediate(4, 17)
    
    def write_r4(self, value):
        self.table.write(5, 17, value)
    
    def read_r4(self):
        return self.table.read_immediate(5, 17)
    
    def write_r5(self, value):
        self.table.write(6, 17, value)
    
    def read_r5(self):
        return self.table.read_immediate(6, 17)
    
    def write_r6(self, value):
        self.table.write(7, 17, value)
    
    def read_r6(self):
        return self.table.read_immediate(7, 17)
    
    def write_r7(self, value):
        self.table.write(8, 17, value)
    
    def read_r7(self):
        return self.table.read_immediate(8, 17)
    
    def write_r8(self, value):
        self.table.write(9, 17, value)
    
    def read_r8(self):
        return self.table.read_immediate(9, 17)
    
    def write_r9(self, value):
        self.table.write(10, 17, value)
    
    def read_r9(self):
        return self.table.read_immediate(10, 17)
    
    def write_r10(self, value):
        self.table.write(11, 17, value)
    
    def read_r10(self):
        return self.table.read_immediate(11, 17)
    
    def write_r11(self, value):
        self.table.write(12, 17, value)
    
    def read_r11(self):
        return self.table.read_immediate(12, 17)
    
    def write_r12(self, value):
        self.table.write(13, 17, value)
    
    def read_r12(self):
        return self.table.read_immediate(13, 17)
    
    def write_r13(self, value):
        self.table.write(14, 17, value)
    
    def read_r13(self):
        return self.table.read_immediate(14, 17)
    
    def write_r14(self, value):
        self.table.write(15, 17, value)
    
    def read_r14(self):
        return self.table.read_immediate(15, 17)
    
    def write_r15(self, value):
        self.table.write(16, 17, value)
    
    def read_r15(self):
        return self.table.read_immediate(16, 17)
    
    #=================================================================================
    # Valores actuales de registros seguros
    #=================================================================================
    def write_w1(self, value):
        self.table.write(1, 20, value)
    
    def read_w1(self):
        return self.table.read_immediate(1, 20)
    
    def write_w2(self, value):
        self.table.write(2, 20, value)
    
    def read_w2(self):
        return self.table.read_immediate(2, 20)
    
    def write_w3(self, value):
        self.table.write(3, 20, value)
    
    def read_w3(self):
        return self.table.read_immediate(3, 20)
    
    def write_w4(self, value):
        self.table.write(4, 20, value)
    
    def read_w4(self):
        return self.table.read_immediate(4, 20)
    
    def write_w5(self, value):
        self.table.write(5, 20, value)
    
    def read_w5(self):
        return self.table.read_immediate(5, 20)
    
    def write_w6(self, value):
        self.table.write(6, 20, value)
    
    def read_w6(self):
        return self.table.read_immediate(6, 20)
    
    def write_w7(self, value):
        self.table.write(7, 20, value)
    
    def read_w7(self):
        return self.table.read_immediate(7, 20)
    
    def write_w8(self, value):
        self.table.write(8, 20, value)
    
    def read_w8(self):
        return self.table.read_immediate(8, 20)
    
    def write_w9(self, value):
        self.table.write(9, 20, value)
    
    def read_w9(self):
        return self.table.read_immediate(9, 20)
    
    def write_d0_safe(self, value):
        self.table.write(10, 20, value)
    
    def read_d0_safe(self):
        return self.table.read_immediate(10, 20)
    
    #=================================================================================
    # Valores actuales de bloques de la contraseña
    #=================================================================================
    def write_p1(self, value):
        self.table.write(1, 23, value)
    
    def read_p1(self):
        return self.table.read_immediate(1, 23)
    
    def write_p2(self, value):
        self.table.write(2, 23, value)
    
    def read_p2(self):
        return self.table.read_immediate(2, 23)
    
    def write_p3(self, value):
        self.table.write(3, 23, value)
    
    def read_p3(self):
        return self.table.read_immediate(3, 23)
    
    def write_p4(self, value):
        self.table.write(4, 23, value)
    
    def read_p4(self):
        return self.table.read_immediate(4, 23)
    
    def write_p5(self, value):
        self.table.write(5, 23, value)
    
    def read_p5(self):
        return self.table.read_immediate(5, 23)
    
    def write_p6(self, value):
        self.table.write(6, 23, value)
    
    def read_p6(self):
        return self.table.read_immediate(6, 23)
    
    def write_p7(self, value):
        self.table.write(7, 23, value)
    
    def read_p7(self):
        return self.table.read_immediate(7, 23)
    
    def write_p8(self, value):
        self.table.write(8, 23, value)
    
    def read_p8(self):
        return self.table.read_immediate(8, 23)
    
    #=================================================================================
    # Valores actuales de la bodega de llaves criptograficas
    #=================================================================================
    def write_k0_0(self, value):
        self.table.write(1, 26, value)
    
    def read_k0_0(self):
        return self.table.read_immediate(1, 26)
    
    def write_k0_1(self, value):
        self.table.write(2, 26, value)
    
    def read_k0_1(self):
        return self.table.read_immediate(2, 26)
    
    def write_k0_2(self, value):
        self.table.write(3, 26, value)
    
    def read_k0_2(self):
        return self.table.read_immediate(3, 26)
    
    def write_k0_3(self, value):
        self.table.write(4, 26, value)
    
    def read_k0_3(self):
        return self.table.read_immediate(4, 26)
    
    def write_k1_0(self, value):
        self.table.write(5, 26, value)
    
    def read_k1_0(self):
        return self.table.read_immediate(5, 26)
    
    def write_k1_1(self, value):
        self.table.write(6, 26, value)
    
    def read_k1_1(self):
        return self.table.read_immediate(6, 26)
    
    def write_k1_2(self, value):
        self.table.write(7, 26, value)
    
    def read_k1_2(self):
        return self.table.read_immediate(7, 26)
    
    def write_k1_3(self, value):
        self.table.write(8, 26, value)
    
    def read_k1_3(self):
        return self.table.read_immediate(8, 26)
    
    def write_k2_0(self, value):
        self.table.write(9, 26, value)
    
    def read_k2_0(self):
        return self.table.read_immediate(9, 26)
    
    def write_k2_1(self, value):
        self.table.write(10, 26, value)
    
    def read_k2_1(self):
        return self.table.read_immediate(10, 26)
    
    def write_k2_2(self, value):
        self.table.write(11, 26, value)
    
    def read_k2_2(self):
        return self.table.read_immediate(11, 26)
    
    def write_k2_3(self, value):
        self.table.write(12, 26, value)
    
    def read_k2_3(self):
        return self.table.read_immediate(12, 26)
    
    def write_k3_0(self, value):
        self.table.write(13, 26, value)
    
    def read_k3_0(self):
        return self.table.read_immediate(13, 26)
    
    def write_k3_1(self, value):
        self.table.write(14, 26, value)
    
    def read_k3_1(self):
        return self.table.read_immediate(14, 26)
    
    def write_k3_2(self, value):
        self.table.write(15, 26, value)
    
    def read_k3_2(self):
        return self.table.read_immediate(15, 26)
    
    def write_k3_3(self, value):
        self.table.write(16, 26, value)
    
    def read_k3_3(self):
        return self.table.read_immediate(16, 26)
    
    #=================================================================================
    # Valores actuales de la memoria general
    #=================================================================================
    def read_memory_block(self, block_index):
        """
        Lee un bloque de memoria de 32 bits.
        
        Args:
            block_index: Índice del bloque (0-63)
        
        Returns:
            int: Valor del bloque o 0x00000000 si fuera de rango
        """
        if block_index < 0 or block_index >= 64:
            return 0x00000000
        
        # Calcular posición en la tabla
        row = self._memory_base_row + block_index
        
        try:
            data_type, value = self.table.read_immediate(row, self._memory_base_col)
            
            if value is None:
                return 0x00000000
            
            # Convertir a entero
            if isinstance(value, str):
                if value.startswith('0x'):
                    return int(value, 16)
                elif value.startswith('0b'):
                    return int(value, 2)
            
            return int(value) & 0xFFFFFFFF
            
        except:
            return 0x00000000

    def write_memory_block(self, block_index, value):
        """
        Escribe un bloque de memoria de 32 bits.
        
        Args:
            block_index: Índice del bloque (0-63)
            value: Valor a escribir
        """
        if block_index < 0 or block_index >= 64:
            return
        
        # Calcular posición en la tabla
        row = self._memory_base_row + block_index
        
        # Asegurar que el valor sea de 32 bits
        value = int(value) & 0xFFFFFFFF
        
        # Escribir en formato hexadecimal
        self.table.write(row, self._memory_base_col, f'0x{value:08X}')

    def read_memory_at_address(self, address):
        """
        Lee datos de la memoria en la dirección especificada.
        
        Args:
            address: Dirección de memoria (binario, decimal o hexadecimal)
        
        Returns:
            str: Valor leído en el mismo formato que la dirección
        """
        size_bits = 32
        try:
            # Detectar formato de entrada
            addr_str = str(address).strip()
            if addr_str.startswith('0b'):
                format_type = 'binary'
            elif addr_str.startswith('0x'):
                format_type = 'hex'
            elif addr_str.startswith('0d'):
                format_type = 'decimal'
            else:
                format_type = 'decimal'
                addr_str = '0d' + addr_str
            
            # Convertir dirección a decimal
            addr_decimal = self._parse_address(address)
            
            if size_bits not in [8, 16, 32]:
                raise ValueError(f"Tamaño no soportado: {size_bits} bits")
            
            size_bytes = size_bits // 8
            
            # Verificar límites
            max_address = 64 * 4  # 256 bytes totales
            if addr_decimal < 0 or addr_decimal >= max_address:
                return self._format_output(0, format_type, size_bits)
            
            # Si la lectura excede el límite, truncar
            if addr_decimal + size_bytes > max_address:
                return self._format_output(0, format_type, size_bits)
            
            # Determinar bloques involucrados
            start_block = addr_decimal // 4
            start_offset = addr_decimal % 4
            end_block = (addr_decimal + size_bytes - 1) // 4
            
            if start_block == end_block:
                # Lectura dentro de un solo bloque
                block_value = self.read_memory_block(start_block)
                
                # Extraer los bits necesarios
                shift = start_offset * 8
                mask = (1 << size_bits) - 1
                result = (block_value >> shift) & mask
                
            else:
                # Lectura cruza bloques
                result = 0
                bits_read = 0
                
                # Primer bloque
                block_value = self.read_memory_block(start_block)
                bits_from_first = (4 - start_offset) * 8
                shift = start_offset * 8
                mask = (1 << bits_from_first) - 1
                result = (block_value >> shift) & mask
                bits_read = bits_from_first
                
                # Bloques intermedios y final
                for block_idx in range(start_block + 1, end_block + 1):
                    block_value = self.read_memory_block(block_idx)
                    
                    if block_idx == end_block:
                        # Último bloque
                        remaining_bits = size_bits - bits_read
                        mask = (1 << remaining_bits) - 1
                        result |= (block_value & mask) << bits_read
                    else:
                        # Bloque completo
                        result |= block_value << bits_read
                        bits_read += 32
            
            return self._format_output(result, format_type, size_bits)
                
        except Exception as e:
            print(f"✗ Error leyendo memoria: {e}")
            return self._format_output(0, 'hex', size_bits)

    def write_memory_at_address(self, address, value):
        """
        Escribe datos en la memoria en la dirección especificada.
        
        Args:
            address: Dirección de memoria (mismo formato que value)
            value: Valor a escribir (mismo formato que address)
        """
        size_bits = 32
        try:
            # Validar que address y value tengan el mismo formato
            addr_str = str(address).strip()
            value_str = str(value).strip()
            
            # Detectar formatos
            addr_format = self._detect_format(addr_str)
            value_format = self._detect_format(value_str)
            
            if addr_format != value_format:
                raise ValueError(f"Address y value deben tener el mismo formato. "
                            f"Address: {addr_format}, Value: {value_format}")
            
            # Parsear valores
            addr_decimal = self._parse_address(address)
            value_decimal = self._parse_value(value, size_bits)
            
            if size_bits not in [8, 16, 32]:
                raise ValueError(f"Tamaño no soportado: {size_bits} bits")
            
            size_bytes = size_bits // 8
            max_address = 64 * 4
            
            if addr_decimal < 0 or addr_decimal >= max_address:
                return
            
            if addr_decimal + size_bytes > max_address:
                return
            
            start_block = addr_decimal // 4
            start_offset = addr_decimal % 4
            end_block = (addr_decimal + size_bytes - 1) // 4
            
            if start_block == end_block:
                # Escritura en un solo bloque
                current_value = self.read_memory_block(start_block)
                
                shift = start_offset * 8
                mask = (1 << size_bits) - 1
                clear_mask = ~(mask << shift) & 0xFFFFFFFF
                
                new_value = (current_value & clear_mask) | ((value_decimal & mask) << shift)
                self.write_memory_block(start_block, new_value)
                
            else:
                # Escritura cruza bloques
                bits_written = 0
                
                # Primer bloque
                current_value = self.read_memory_block(start_block)
                bits_in_first = (4 - start_offset) * 8
                shift = start_offset * 8
                
                preserve_low = (1 << shift) - 1
                preserve_high = ~((1 << (shift + bits_in_first)) - 1) & 0xFFFFFFFF
                value_part = value_decimal & ((1 << bits_in_first) - 1)
                
                new_value = (current_value & preserve_low) | (value_part << shift) | (current_value & preserve_high)
                self.write_memory_block(start_block, new_value)
                
                value_decimal >>= bits_in_first
                bits_written = bits_in_first
                
                # Bloques siguientes
                for block_idx in range(start_block + 1, end_block + 1):
                    current_value = self.read_memory_block(block_idx)
                    
                    if block_idx == end_block:
                        # Último bloque
                        remaining_bits = size_bits - bits_written
                        mask = (1 << remaining_bits) - 1
                        preserve_mask = ~mask & 0xFFFFFFFF
                        
                        new_value = (value_decimal & mask) | (current_value & preserve_mask)
                        self.write_memory_block(block_idx, new_value)
                    else:
                        # Bloque completo
                        self.write_memory_block(block_idx, value_decimal & 0xFFFFFFFF)
                        value_decimal >>= 32
            
            # Ejecutar escrituras pendientes
            self.table.execute_writes_only()
            
        except Exception as e:
            print(f"✗ Error escribiendo memoria: {e}")

    def _parse_address(self, address):
        """Convierte una dirección en cualquier formato a decimal"""
        addr_str = str(address).strip()
        
        if addr_str.startswith('0b'):
            return int(addr_str, 2)
        elif addr_str.startswith('0x'):
            return int(addr_str, 16)
        elif addr_str.startswith('0d'):
            return int(addr_str[2:])
        else:
            return int(addr_str)

    def _detect_format(self, value_str):
        """Detecta el formato de un string de valor"""
        if value_str.startswith('0b'):
            return 'binary'
        elif value_str.startswith('0x'):
            return 'hex'
        elif value_str.startswith('0d'):
            return 'decimal'
        else:
            # Si no tiene prefijo, asumir decimal
            return 'decimal'

    def _parse_value(self, value, size_bits):
        """
        Parsea un valor y aplica complemento a 2 si es necesario.
        Solo aplica complemento a 2 para valores decimales.
        """
        value_str = str(value).strip()
        
        if value_str.startswith('0b'):
            # Binario - asumir que ya tiene complemento a 2
            return int(value_str, 2) & ((1 << size_bits) - 1)
        elif value_str.startswith('0x'):
            # Hexadecimal - asumir que ya tiene complemento a 2
            return int(value_str, 16) & ((1 << size_bits) - 1)
        elif value_str.startswith('0d'):
            # Decimal con prefijo
            decimal_value = int(value_str[2:])
            return self._apply_two_complement(decimal_value, size_bits)
        else:
            # Decimal sin prefijo
            decimal_value = int(value_str)
            return self._apply_two_complement(decimal_value, size_bits)

    def _apply_two_complement(self, value, size_bits):
        """
        Aplica complemento a 2 para valores decimales con signo.
        Rangos válidos:
        - 8 bits: -128 a 127
        - 16 bits: -32,768 a 32,767
        - 32 bits: -2,147,483,648 a 2,147,483,647
        """
        # Calcular límites
        max_positive = (1 << (size_bits - 1)) - 1
        min_negative = -(1 << (size_bits - 1))
        
        # Validar rango
        if value < min_negative or value > max_positive:
            raise ValueError(f"Valor {value} fuera de rango para {size_bits} bits "
                            f"({min_negative} a {max_positive})")
        
        # Si es negativo, aplicar complemento a 2
        if value < 0:
            return (1 << size_bits) + value
        else:
            return value

    def _format_output(self, value, format_type, size_bits):
        """
        Formatea el valor de salida según el tipo especificado.
        Para decimal, convierte de complemento a 2 a valor con signo.
        """
        # Asegurar que el valor esté en el rango correcto
        value = value & ((1 << size_bits) - 1)
        
        if format_type == 'binary':
            return f"0b{value:0{size_bits}b}"
        elif format_type == 'hex':
            hex_digits = (size_bits + 3) // 4  # Redondear hacia arriba
            return f"0x{value:0{hex_digits}X}"
        else:  # decimal
            # Convertir de complemento a 2 a valor con signo
            if value & (1 << (size_bits - 1)):  # Si el bit más significativo es 1
                # Es negativo en complemento a 2
                signed_value = value - (1 << size_bits)
            else:
                signed_value = value
            return f"0d{signed_value}"

    # Métodos de compatibilidad para migración gradual
    def read_g(self, index):
        """Compatibilidad con código existente"""
        return (DataType.HEX, self.read_memory_block(index))

    def write_g(self, index, value):
        """Compatibilidad con código existente"""
        self.write_memory_block(index, value)
        
    # ===== MEMORIA DINÁMICA =====
    def read_dynamic_memory(self, address):
        """
        Lee un bloque de 32 bits de la memoria dinámica.
        
        Args:
            address: Dirección en formato binario, decimal o hexadecimal
            
        Returns:
            str: Valor leído en el mismo formato que la dirección
        """
        try:
            # Detectar formato de entrada
            addr_str = str(address).strip()
            format_type = self._detect_format(addr_str)
            if format_type == 'decimal' and not addr_str.startswith('0d'):
                addr_str = '0d' + addr_str
            
            # Convertir dirección a decimal
            addr_decimal = self._parse_address(address)
            
            # Construir ruta al archivo
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            parent_dir = current_dir.parent
            bin_file = parent_dir / "Assets" / "dynamic_mem.bin"
            
            # Si no existe el archivo, retornar 0
            if not bin_file.exists():
                return self._format_output(0, format_type, 32)
            
            # Leer del archivo
            with open(bin_file, 'rb') as f:
                f.seek(addr_decimal)
                data = f.read(4)
                
                if len(data) < 4:
                    # No hay suficientes datos
                    return self._format_output(0, format_type, 32)
                
                # Convertir bytes a entero (little-endian)
                value = int.from_bytes(data, byteorder='little', signed=False)
                
            return self._format_output(value, format_type, 32)
            
        except Exception as e:
            print(f"✗ Error leyendo memoria dinámica: {e}")
            return self._format_output(0, format_type if 'format_type' in locals() else 'hex', 32)

    def write_dynamic_memory(self, address, value):
        """
        Escribe un bloque de 32 bits en la memoria dinámica.
        
        Args:
            address: Dirección (mismo formato que value)
            value: Valor a escribir (mismo formato que address)
        """
        try:
            # Validar formatos
            addr_str = str(address).strip()
            value_str = str(value).strip()
            
            addr_format = self._detect_format(addr_str)
            value_format = self._detect_format(value_str)
            
            if addr_format != value_format:
                raise ValueError(f"Address y value deben tener el mismo formato. "
                            f"Address: {addr_format}, Value: {value_format}")
            
            # Parsear valores
            addr_decimal = self._parse_address(address)
            value_decimal = self._parse_value(value, 32)
            
            # Construir ruta
            current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            parent_dir = current_dir.parent
            assets_dir = parent_dir / "Assets"
            bin_file = assets_dir / "dynamic_mem.bin"
            
            # Crear directorio si no existe
            os.makedirs(assets_dir, exist_ok=True)
            
            # Si el archivo no existe o es muy pequeño, expandirlo
            if not bin_file.exists():
                with open(bin_file, 'wb') as f:
                    # Crear archivo con ceros
                    f.write(b'\x00' * (addr_decimal + 4))
            else:
                # Verificar tamaño actual
                current_size = os.path.getsize(bin_file)
                if current_size < addr_decimal + 4:
                    # Expandir archivo
                    with open(bin_file, 'ab') as f:
                        f.write(b'\x00' * (addr_decimal + 4 - current_size))
            
            # Escribir los 4 bytes
            with open(bin_file, 'r+b') as f:
                f.seek(addr_decimal)
                f.write(value_decimal.to_bytes(4, byteorder='little', signed=False))
            
            print(f"✓ Escrito en memoria dinámica [{address}] = {value}")
            
        except Exception as e:
            print(f"✗ Error escribiendo memoria dinámica: {e}")
    
        
    #=================================================================================
    # Valor de la instruccion actual por estado
    #=================================================================================
    def write_state_fetch(self, value):
        self.table.write(42, 1, value)
    
    def read_state_fetch(self):
        return self.table.read_immediate(42, 1)
        
    def write_state_decode(self, value):
        self.table.write(42, 4, value)
    
    def read_state_decode(self):
        return self.table.read_immediate(42, 4)
    
    def write_state_execute(self, value):
        self.table.write(42, 7, value)
    
    def read_state_execute(self):
        return self.table.read_immediate(42, 7)
    
    def write_state_memory(self, value):
        self.table.write(42, 10, value)
    
    def read_state_memory(self):
        return self.table.read_immediate(42, 10)
    
    def write_state_writeBack(self, value):
        self.table.write(42, 13, value)
    
    def read_state_writeBack(self):
        return self.table.read_immediate(42, 13)
    
    #=================================================================================
    # Valores del timer e intentos
    #=================================================================================
    def write_timer_safe(self, value):
        self.table.write(42, 16, value)
    
    def read_timer_safe(self):
        return self.table.read_immediate(42, 16)
    
    def write_block_statusIn(self, value):
        self.table.write(43, 16, value)
    
    def read_block_statusIn(self):
        return self.table.read_immediate(43, 16)
    
    def write_block_statusOut(self, value):
        self.table.write(44, 16, value)
    
    def read_block_statusOut(self):
        return self.table.read_immediate(44, 16)
    
    def write_attempts_available(self, value):
        self.table.write(42, 19, value)
    
    def read_attempts_available(self):
        return self.table.read_immediate(42, 19)
        
    #=================================================================================
    # Funcion de reset para el inicio del simulador
    #=================================================================================
    def reset(self, full=False):
        """Resetea todas las señales a sus valores iniciales y escribe sus nombres"""
        # Señales del Decode
        # Write string (etiquetas)
        self.table.write(1, 1, "PC'")
        self.table.write(2, 1, "PCF")
        self.table.write(3, 1, "PCPlus8F")
        self.table.write(4, 1, "InstrF")
        # Write numérico (valores iniciales) usando funciones para Decode
        self.write_pc_prime("0x00000000")
        self.write_pcf("0x00000000")
        self.write_pcplus8f("0x00001000")
        self.write_instrf("0x300000000000000")
        
        # Señales del Fetch
        # Write string (etiquetas)
        self.table.write(1, 4, "InstrD")
        self.table.write(2, 4, "PCF_D")
        self.table.write(3, 4, "55:52")
        self.table.write(4, 4, "63:56")
        self.table.write(5, 4, "47:44")
        self.table.write(6, 4, "43:40")
        self.table.write(7, 4, "39:8")
        self.table.write(8, 4, "51:48")
        self.table.write(9, 4, "MemWriteP")
        self.table.write(10, 4, "MemWriteV")
        self.table.write(11, 4, "RegisterInA")
        self.table.write(12, 4, "RegisterInB")
        self.table.write(13, 4, "ImmediateOp")
        self.table.write(14, 4, "BranchE")
        self.table.write(15, 4, "LogOutD")
        self.table.write(16, 4, "ComSD")
        self.table.write(17, 4, "PrintEnD")
        self.table.write(18, 4, "RegWriteSD")
        self.table.write(19, 4, "RegWriteRD")
        self.table.write(20, 4, "MemOpD")
        self.table.write(21, 4, "MemWriteGD")
        self.table.write(22, 4, "MemWriteDD")
        self.table.write(23, 4, "MemByteD")
        self.table.write(24, 4, "PCSrcD")
        self.table.write(25, 4, "FlagsUpdD")
        self.table.write(26, 4, "ALUSrcD")
        self.table.write(27, 4, "BranchOpD")
        self.table.write(28, 4, "RDr1_a")
        self.table.write(29, 4, "RDr2_a")
        self.table.write(30, 4, "RDw1_a")
        self.table.write(31, 4, "RDw2_a")
        self.table.write(32, 4, "KD_a")
        self.table.write(33, 4, "RD_a")
        self.table.write(34, 4, "SrcAD_0")
        self.table.write(35, 4, "SrcAD")
        self.table.write(36, 4, "Rd_SpecialD")
        self.table.write(37, 4, "SrcBD")
        # Write numérico (valores iniciales) utilizando las funciones del Decode
        self.write_instrd("0x300000000000000")
        self.write_pcf_d("0x00000000")
        self.write_55_52("0b0000")
        self.write_63_56("0b00110000")
        self.write_47_44("0b0000")
        self.write_43_40("0b0000")
        self.write_39_8("0x00000000")
        self.write_51_48("0b0000")
        self.write_memwritep("0b0")
        self.write_memwritev("0b0")
        self.write_registerina("0b1")
        self.write_registerinb("0b00")
        self.write_immediateop("0b0")
        self.write_branche("0b0")
        self.write_logoutd("0b0")
        self.write_comsd("0b0")
        self.write_printend("0b11")
        self.write_regwritesd("0b0")
        self.write_regwriterd("0b0")
        self.write_memopd("0b11")
        self.write_memwritegd("0b0")
        self.write_memwritedd("0b0")
        self.write_membyted("0b0")
        self.write_pcsrcd("0b0")
        self.write_flagsupdd("0b0")
        self.write_alusrcd("0b000000")
        self.write_branchopd("0b111")
        self.write_rdr1_a("0x00000000")
        self.write_rdr2_a("0x00000000")
        self.write_rdw1_a("0x00000000")
        self.write_rdw2_a("0x00000000")
        self.write_kd_a("0x00000000")
        self.write_rd_a("0x00000000")
        self.write_srcad_0("0x00000000")
        self.write_srcad("0x00000000")
        self.write_rd_speciald("0x00000000")
        self.write_srcbd("0x00000000")
        
        # Señales del Execute
        # Write string (etiquetas)
        self.table.write(1, 7, "RegWriteSE")
        self.table.write(2, 7, "RegWriteRE")
        self.table.write(3, 7, "MemOpE")
        self.table.write(4, 7, "MemWriteGE")
        self.table.write(5, 7, "MemWriteDE")
        self.table.write(6, 7, "MemByteE")
        self.table.write(7, 7, "PCSrcE")
        self.table.write(8, 7, "FlagsUpdE")
        self.table.write(9, 7, "ALUSrcE")
        self.table.write(10, 7, "BranchOpE")
        self.table.write(11, 7, "PrintEnE")
        self.table.write(12, 7, "ComSE")
        self.table.write(13, 7, "LogOutE")
        self.table.write(14, 7, "BranchOpE")
        self.table.write(15, 7, "FlagsE")
        self.table.write(16, 7, "SrcAE")
        self.table.write(17, 7, "RD_SpecialE")
        self.table.write(18, 7, "SrcBE")
        self.table.write(19, 7, "Flags'")
        self.table.write(20, 7, "ALUFlagOut")
        self.table.write(21, 7, "CarryIn")
        self.table.write(22, 7, "CondExE")
        self.table.write(23, 7, "SafeFlagsOut")
        self.table.write(24, 7, "LoginInBlockE")
        self.table.write(25, 7, "RdE")
        self.table.write(26, 7, "ALUResultE")
        self.table.write(27, 7, "PCSrc_AND_E")
        # Write numérico (valores iniciales)
        self.write_regwritese("0b0")
        self.write_regwritere("0b0")
        self.write_memope("0b11")
        self.write_memwritege("0b0")
        self.write_memwritede("0b0")
        self.write_membytee("0b0")
        self.write_pcsrce("0b0")
        self.write_flagsupde("0b0")
        self.write_alusrce("0b000000")
        self.write_branchope("0b111")
        self.write_printene("0b11")
        self.write_comse("0b0")
        self.write_logoute("0b0")
        self.write_branchope_2("0b111")
        self.write_flagse("0b0000")
        self.write_srcae("0x00000000")
        self.write_rd_speciale("0x00000000")
        self.write_srcbe("0x00000000")
        self.write_flags_prime("0b0000")
        self.write_aluflagout("0b0000")
        self.write_carryin("0b0")
        self.write_condexe("0b0")
        self.write_safeflagsout("0b00")
        self.write_logininblocke("0b0000")
        self.write_rde("0b0000")
        self.write_aluresulte("0x00000000")
        self.write_pcsrc_and_e("0b0")
        
        # Señales del Memory
        # Write string (etiquetas)
        self.table.write(1, 10, "RegWriteSM")
        self.table.write(2, 10, "RegWriteRM")
        self.table.write(3, 10, "MemOpM")
        self.table.write(4, 10, "MemWriteGM")
        self.table.write(5, 10, "MemWriteDM")
        self.table.write(6, 10, "MemByteM")
        self.table.write(7, 10, "PCSrcM")
        self.table.write(8, 10, "PrintEnM")
        self.table.write(9, 10, "ALUOutM")
        self.table.write(10, 10, "RD_SpecialM")
        self.table.write(11, 10, "RdM")
        self.table.write(12, 10, "RD_SpecialM_b")
        self.table.write(13, 10, "RD_SpecialM_c")
        self.table.write(14, 10, "RD_SpecialM_d")
        self.table.write(15, 10, "RD_SpecialM_e")
        self.table.write(16, 10, "RD_G_a")
        self.table.write(17, 10, "RD_D_a")
        self.table.write(18, 10, "ALUOutM_O")
        # Write numérico (valores iniciales)
        self.write_regwritesm("0b0")
        self.write_regwriterm("0b0")
        self.write_memopm("0b11")
        self.write_memwritegm("0b0")
        self.write_memwritedm("0b0")
        self.write_membytem("0b0")
        self.write_pcsrcm("0b0")
        self.write_printenm("0b11")
        self.write_aluoutm("0x00000000")
        self.write_rd_specialm("0x00000000")
        self.write_rdm("0b0000")
        self.write_rd_specialm_b("0x00000000")
        self.write_rd_specialm_c("0x00000000")
        self.write_rd_specialm_d("0x00000000")
        self.write_rd_specialm_e("0x00000000")
        self.write_rd_g_a("0x00000000")
        self.write_rd_d_a("0x00000000")
        self.write_aluoutm_o("0x00000000")
        
        # Señales del WriteBack
        # Write string (etiquetas)
        self.table.write(1, 13, "RegWriteSM")
        self.table.write(2, 13, "RegWriteRM")
        self.table.write(3, 13, "PCSrcM")
        self.table.write(4, 13, "MemByteM")
        self.table.write(5, 13, "PrintEnM")
        self.table.write(6, 13, "ALUOutW")
        self.table.write(7, 13, "ALUOutW_b")
        self.table.write(8, 13, "ALUOutW_c")
        self.table.write(9, 13, "int_pl")
        self.table.write(10, 13, "ACII_pl")
        self.table.write(11, 13, "b_pl")
        self.table.write(12, 13, "RdW")
        # Write numérico (valores iniciales) utilizando las funciones del WriteBack
        self.write_regwritesm_wb("0b0")
        self.write_regwriterm_wb("0b0")
        self.write_pcsrcm_wb("0b0")
        self.write_membytem_wb("0b0")
        self.write_printenm_wb("0b11")
        self.write_aluoutw("0x00000000")
        self.write_aluoutw_b("0x00000000")
        self.write_aluoutw_c("0x00000000")
        self.write_int_pl("0x00000000")
        self.write_acii_pl("0x00000000")
        self.write_b_pl("0x00000000")
        self.write_rdw("0b0000")
        
        # Valores actuales de registros generales
        # Write string (nombres de registros)
        self.table.write(1, 16, "R0")
        self.table.write(2, 16, "R1")
        self.table.write(3, 16, "R2")
        self.table.write(4, 16, "R3")
        self.table.write(5, 16, "R4")
        self.table.write(6, 16, "R5")
        self.table.write(7, 16, "R6")
        self.table.write(8, 16, "R7")
        self.table.write(9, 16, "R8")
        self.table.write(10, 16, "R9")
        self.table.write(11, 16, "R10")
        self.table.write(12, 16, "R11")
        self.table.write(13, 16, "R12")
        self.table.write(14, 16, "R13")
        self.table.write(15, 16, "R14")
        self.table.write(16, 16, "R15")
        # Write numérico (valores iniciales) de registros generales usando funciones
        self.write_r0("0x00000000")
        self.write_r1("0x00000000")
        self.write_r2("0x00000000")
        self.write_r3("0x00000000")
        self.write_r4("0x00000000")
        self.write_r5("0x00000000")
        self.write_r6("0x00000000")
        self.write_r7("0x00000000")
        self.write_r8("0x00000000")
        self.write_r9("0x00000000")
        self.write_r10("0x00000000")
        self.write_r11("0x00000000")
        self.write_r12("0x00000000")
        self.write_r13("0x00000000")
        self.write_r14("0x00000000")
        self.write_r15("0x00000000")
        
        # Valores actuales de registros seguros
        # Write string (nombres)
        self.table.write(1, 19, "W1")
        self.table.write(2, 19, "W2")
        self.table.write(3, 19, "W3")
        self.table.write(4, 19, "W4")
        self.table.write(5, 19, "W5")
        self.table.write(6, 19, "W6")
        self.table.write(7, 19, "W7")
        self.table.write(8, 19, "W8")
        self.table.write(9, 19, "W9")
        self.table.write(10, 19, "D0")
        # Write numérico (valores iniciales) usando funciones
        self.write_w1("0x00000000")
        self.write_w2("0x00000000")
        self.write_w3("0x00000000")
        self.write_w4("0x00000000")
        self.write_w5("0x00000000")
        self.write_w6("0x00000000")
        self.write_w7("0x00000000")
        self.write_w8("0x00000000")
        self.write_w9("0x00000000")
        self.write_d0_safe("0x9E3779B9")
        
        # Valores actuales de bloques de la contraseña
        # Write string (nombres de bloques)
        self.table.write(1, 22, "P1")
        self.table.write(2, 22, "P2")
        self.table.write(3, 22, "P3")
        self.table.write(4, 22, "P4")
        self.table.write(5, 22, "P5")
        self.table.write(6, 22, "P6")
        self.table.write(7, 22, "P7")
        self.table.write(8, 22, "P8")
        
        # Valores actuales de memoria de llaves criptograficas k
        # Write string (nombres de registros k)
        self.table.write(1, 25, "k0.0")
        self.table.write(2, 25, "k0.1")
        self.table.write(3, 25, "k0.2")
        self.table.write(4, 25, "k0.3")
        self.table.write(5, 25, "k1.0")
        self.table.write(6, 25, "k1.1")
        self.table.write(7, 25, "k1.2")
        self.table.write(8, 25, "k1.3")
        self.table.write(9, 25, "k2.0")
        self.table.write(10, 25, "k2.1")
        self.table.write(11, 25, "k2.2")
        self.table.write(12, 25, "k2.3")
        self.table.write(13, 25, "k3.0")
        self.table.write(14, 25, "k3.1")
        self.table.write(15, 25, "k3.2")
        self.table.write(16, 25, "k3.3")
        
        # Estado regular de la instrucción actual por estado
        #Nombres de los estados
        self.table.write(41, 1, "Fetch:")
        self.table.write(41, 4, "Decode:")
        self.table.write(41, 7, "Execute:")
        self.table.write(41, 10, "Memory:")
        self.table.write(41, 13, "WriteBack:")
        # Valores iniciales de los estados
        self.write_state_fetch("NOP")
        self.write_state_decode("NOP")
        self.write_state_execute("NOP")
        self.write_state_memory("NOP")
        self.write_state_writeBack("NOP")

        # Estado regular del timer e intentos
        # Write string
        self.table.write(42, 15, "Timer Value")
        self.table.write(43, 15, "Block Status In")
        self.table.write(44, 15, "Block Status Out")
        self.table.write(42, 18, "Intentos")
        
        if full:
            # Establecer todos los bloques de memoria general
            for row in range(1, 65):
                self.table.write(row, 28, f"G{row-1}")
                self.table.write(row, 29, "0x00000000")
            
            #Reiniciar valores de seguridad
            self.write_timer_safe(0)
            self.write_block_statusIn("0b00000000")
            self.write_block_statusOut("0b00000000")
            self.write_attempts_available("0b0000")
            
            # Write numérico de llaves criptograficas (valores iniciales) usando funciones
            self.write_k0_0("0x00000000")
            self.write_k0_1("0x00000000")
            self.write_k0_2("0x00000000")
            self.write_k0_3("0x00000000")
            self.write_k1_0("0x00000000")
            self.write_k1_1("0x00000000")
            self.write_k1_2("0x00000000")
            self.write_k1_3("0x00000000")
            self.write_k2_0("0x00000000")
            self.write_k2_1("0x00000000")
            self.write_k2_2("0x00000000")
            self.write_k2_3("0x00000000")
            self.write_k3_0("0x00000000")
            self.write_k3_1("0x00000000")
            self.write_k3_2("0x00000000")
            self.write_k3_3("0x00000000")
            
            # Write numérico (valores iniciales) usando funciones de la contraseña
            self.write_p1("0x00000001")
            self.write_p2("0x00000010")
            self.write_p3("0x00000011")
            self.write_p4("0x00000100")
            self.write_p5("0x00000101")
            self.write_p6("0x00000110")
            self.write_p7("0x00000111")
            self.write_p8("0x00001000")

        self.table.execute_all()