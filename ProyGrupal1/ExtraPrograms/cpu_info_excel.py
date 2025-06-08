import os
import sys
from pathlib import Path

# Añadir el directorio actual al path para imports relativos
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(current_dir))

from table_control import TableControl

class CPUInfoExcel:
    """Clase para manejar la lectura y escritura de señales del CPU en Excel"""
    
    def __init__(self):
        self.table = TableControl()
    
    #=================================================================================
    # Señales del Decode
    #=================================================================================
    def write_pc_prime(self, value):
        self.table.write(1, 2, value)
    
    def read_pc_prime(self, callback=None):
        self.table.read(1, 2, callback)
    
    def write_pcf(self, value):
        self.table.write(2, 2, value)
    
    def read_pcf(self, callback=None):
        self.table.read(2, 2, callback)
    
    def write_pcplus8f(self, value):
        self.table.write(3, 2, value)
    
    def read_pcplus8f(self, callback=None):
        self.table.read(3, 2, callback)
    
    def write_instrf(self, value):
        self.table.write(4, 2, value)
    
    def read_instrf(self, callback=None):
        self.table.read(4, 2, callback)
    
    # Señales del Fetch
    def write_instrd(self, value):
        self.table.write(1, 5, value)
    
    def read_instrd(self, callback=None):
        self.table.read(1, 5, callback)
    
    def write_pcf_d(self, value):
        self.table.write(2, 5, value)
    
    def read_pcf_d(self, callback=None):
        self.table.read(2, 5, callback)
    
    def write_55_52(self, value):
        self.table.write(3, 5, value)
    
    def read_55_52(self, callback=None):
        self.table.read(3, 5, callback)
    
    def write_63_56(self, value):
        self.table.write(4, 5, value)
    
    def read_63_56(self, callback=None):
        self.table.read(4, 5, callback)
    
    def write_47_44(self, value):
        self.table.write(5, 5, value)
    
    def read_47_44(self, callback=None):
        self.table.read(5, 5, callback)
    
    def write_43_40(self, value):
        self.table.write(6, 5, value)
    
    def read_43_40(self, callback=None):
        self.table.read(6, 5, callback)
    
    def write_39_8(self, value):
        self.table.write(7, 5, value)
    
    def read_39_8(self, callback=None):
        self.table.read(7, 5, callback)
    
    def write_51_48(self, value):
        self.table.write(8, 5, value)
    
    def read_51_48(self, callback=None):
        self.table.read(8, 5, callback)
    
    def write_memwritep(self, value):
        self.table.write(9, 5, value)
    
    def read_memwritep(self, callback=None):
        self.table.read(9, 5, callback)
    
    def write_memwritev(self, value):
        self.table.write(10, 5, value)
    
    def read_memwritev(self, callback=None):
        self.table.read(10, 5, callback)
    
    def write_registerina(self, value):
        self.table.write(11, 5, value)
    
    def read_registerina(self, callback=None):
        self.table.read(11, 5, callback)
    
    def write_registerinb(self, value):
        self.table.write(12, 5, value)
    
    def read_registerinb(self, callback=None):
        self.table.read(12, 5, callback)
    
    def write_immediateop(self, value):
        self.table.write(13, 5, value)
    
    def read_immediateop(self, callback=None):
        self.table.read(13, 5, callback)
    
    def write_branche(self, value):
        self.table.write(14, 5, value)
    
    def read_branche(self, callback=None):
        self.table.read(14, 5, callback)
    
    def write_logoutd(self, value):
        self.table.write(15, 5, value)
    
    def read_logoutd(self, callback=None):
        self.table.read(15, 5, callback)
    
    def write_comsd(self, value):
        self.table.write(16, 5, value)
    
    def read_comsd(self, callback=None):
        self.table.read(16, 5, callback)
    
    def write_printend(self, value):
        self.table.write(17, 5, value)
    
    def read_printend(self, callback=None):
        self.table.read(17, 5, callback)
    
    def write_regwritesd(self, value):
        self.table.write(18, 5, value)
    
    def read_regwritesd(self, callback=None):
        self.table.read(18, 5, callback)
    
    def write_regwriterd(self, value):
        self.table.write(19, 5, value)
    
    def read_regwriterd(self, callback=None):
        self.table.read(19, 5, callback)
    
    def write_memopd(self, value):
        self.table.write(21, 5, value)
    
    def read_memopd(self, callback=None):
        self.table.read(21, 5, callback)
    
    def write_memwritegd(self, value):
        self.table.write(22, 5, value)
    
    def read_memwritegd(self, callback=None):
        self.table.read(22, 5, callback)
    
    def write_memwritedd(self, value):
        self.table.write(23, 5, value)
    
    def read_memwritedd(self, callback=None):
        self.table.read(23, 5, callback)
    
    def write_membyted(self, value):
        self.table.write(24, 5, value)
    
    def read_membyted(self, callback=None):
        self.table.read(24, 5, callback)
    
    def write_pcsrcd(self, value):
        self.table.write(25, 5, value)
    
    def read_pcsrcd(self, callback=None):
        self.table.read(25, 5, callback)
    
    def write_flagsupdd(self, value):
        self.table.write(26, 5, value)
    
    def read_flagsupdd(self, callback=None):
        self.table.read(26, 5, callback)
    
    def write_alusrcd(self, value):
        self.table.write(27, 5, value)
    
    def read_alusrcd(self, callback=None):
        self.table.read(27, 5, callback)
    
    def write_branchopd(self, value):
        self.table.write(28, 5, value)
    
    def read_branchopd(self, callback=None):
        self.table.read(28, 5, callback)
    
    def write_rdr1_a(self, value):
        self.table.write(29, 5, value)
    
    def read_rdr1_a(self, callback=None):
        self.table.read(29, 5, callback)
    
    def write_rdr2_a(self, value):
        self.table.write(30, 5, value)
    
    def read_rdr2_a(self, callback=None):
        self.table.read(30, 5, callback)
    
    def write_rdw1_a(self, value):
        self.table.write(31, 5, value)
    
    def read_rdw1_a(self, callback=None):
        self.table.read(31, 5, callback)
    
    def write_rdw2_a(self, value):
        self.table.write(32, 5, value)
    
    def read_rdw2_a(self, callback=None):
        self.table.read(32, 5, callback)
    
    def write_kd_a(self, value):
        self.table.write(33, 5, value)
    
    def read_kd_a(self, callback=None):
        self.table.read(33, 5, callback)
    
    def write_rd_a(self, value):
        self.table.write(34, 5, value)
    
    def read_rd_a(self, callback=None):
        self.table.read(34, 5, callback)
    
    def write_srcad_0(self, value):
        self.table.write(35, 5, value)
    
    def read_srcad_0(self, callback=None):
        self.table.read(35, 5, callback)
    
    def write_srcad(self, value):
        self.table.write(36, 5, value)
    
    def read_srcad(self, callback=None):
        self.table.read(36, 5, callback)
    
    def write_rd_speciald(self, value):
        self.table.write(37, 5, value)
    
    def read_rd_speciald(self, callback=None):
        self.table.read(37, 5, callback)
    
    def write_srcbd(self, value):
        self.table.write(38, 5, value)
    
    def read_srcbd(self, callback=None):
        self.table.read(38, 5, callback)
    
    #=================================================================================
    # Señales del Execute
    #=================================================================================
    def write_regwritese(self, value):
        self.table.write(1, 8, value)
    
    def read_regwritese(self, callback=None):
        self.table.read(1, 8, callback)
    
    def write_regwritere(self, value):
        self.table.write(2, 8, value)
    
    def read_regwritere(self, callback=None):
        self.table.read(2, 8, callback)
    
    def write_memope(self, value):
        self.table.write(3, 8, value)
    
    def read_memope(self, callback=None):
        self.table.read(3, 8, callback)
    
    def write_memwritege(self, value):
        self.table.write(4, 8, value)
    
    def read_memwritege(self, callback=None):
        self.table.read(4, 8, callback)
    
    def write_memwritede(self, value):
        self.table.write(5, 8, value)
    
    def read_memwritede(self, callback=None):
        self.table.read(5, 8, callback)
    
    def write_membytee(self, value):
        self.table.write(6, 8, value)
    
    def read_membytee(self, callback=None):
        self.table.read(6, 8, callback)
    
    def write_pcsrce(self, value):
        self.table.write(7, 8, value)
    
    def read_pcsrce(self, callback=None):
        self.table.read(7, 8, callback)
    
    def write_flagsupde(self, value):
        self.table.write(8, 8, value)
    
    def read_flagsupde(self, callback=None):
        self.table.read(8, 8, callback)
    
    def write_alusrce(self, value):
        self.table.write(9, 8, value)
    
    def read_alusrce(self, callback=None):
        self.table.read(9, 8, callback)
    
    def write_branchope(self, value):
        self.table.write(10, 8, value)
    
    def read_branchope(self, callback=None):
        self.table.read(10, 8, callback)
    
    def write_printene(self, value):
        self.table.write(11, 8, value)
    
    def read_printene(self, callback=None):
        self.table.read(11, 8, callback)
    
    def write_comse(self, value):
        self.table.write(12, 8, value)
    
    def read_comse(self, callback=None):
        self.table.read(12, 8, callback)
    
    def write_logoute(self, value):
        self.table.write(13, 8, value)
    
    def read_logoute(self, callback=None):
        self.table.read(13, 8, callback)
    
    def write_branchope_2(self, value):
        self.table.write(14, 8, value)
    
    def read_branchope_2(self, callback=None):
        self.table.read(14, 8, callback)
    
    def write_flagse(self, value):
        self.table.write(15, 8, value)
    
    def read_flagse(self, callback=None):
        self.table.read(15, 8, callback)
    
    def write_srcae(self, value):
        self.table.write(16, 8, value)
    
    def read_srcae(self, callback=None):
        self.table.read(16, 8, callback)
    
    def write_rd_speciale(self, value):
        self.table.write(17, 8, value)
    
    def read_rd_speciale(self, callback=None):
        self.table.read(17, 8, callback)
    
    def write_srcbe(self, value):
        self.table.write(18, 8, value)
    
    def read_srcbe(self, callback=None):
        self.table.read(18, 8, callback)
    
    def write_flags_prime(self, value):
        self.table.write(19, 8, value)
    
    def read_flags_prime(self, callback=None):
        self.table.read(19, 8, callback)
    
    def write_aluflagout(self, value):
        self.table.write(20, 8, value)
    
    def read_aluflagout(self, callback=None):
        self.table.read(20, 8, callback)
    
    def write_carryin(self, value):
        self.table.write(21, 8, value)
    
    def read_carryin(self, callback=None):
        self.table.read(21, 8, callback)
    
    def write_condexe(self, value):
        self.table.write(22, 8, value)
    
    def read_condexe(self, callback=None):
        self.table.read(22, 8, callback)
    
    def write_safeflagsout(self, value):
        self.table.write(23, 8, value)
    
    def read_safeflagsout(self, callback=None):
        self.table.read(23, 8, callback)
    
    def write_logininblocke(self, value):
        self.table.write(24, 8, value)
    
    def read_logininblocke(self, callback=None):
        self.table.read(24, 8, callback)
    
    def write_rde(self, value):
        self.table.write(25, 8, value)
    
    def read_rde(self, callback=None):
        self.table.read(25, 8, callback)
    
    def write_aluresulte(self, value):
        self.table.write(26, 8, value)
    
    def read_aluresulte(self, callback=None):
        self.table.read(26, 8, callback)
    
    def write_pcsrc_and_e(self, value):
        self.table.write(27, 8, value)
    
    def read_pcsrc_and_e(self, callback=None):
        self.table.read(27, 8, callback)
    
    #=================================================================================
    # Señales del Memory
    #=================================================================================
    def write_regwritesm(self, value):
        self.table.write(1, 11, value)
    
    def read_regwritesm(self, callback=None):
        self.table.read(1, 11, callback)
    
    def write_regwriterm(self, value):
        self.table.write(2, 11, value)
    
    def read_regwriterm(self, callback=None):
        self.table.read(2, 11, callback)
    
    def write_memopm(self, value):
        self.table.write(3, 11, value)
    
    def read_memopm(self, callback=None):
        self.table.read(3, 11, callback)
    
    def write_memwritegm(self, value):
        self.table.write(4, 11, value)
    
    def read_memwritegm(self, callback=None):
        self.table.read(4, 11, callback)
    
    def write_memwritedm(self, value):
        self.table.write(5, 11, value)
    
    def read_memwritedm(self, callback=None):
        self.table.read(5, 11, callback)
    
    def write_membytem(self, value):
        self.table.write(6, 11, value)
    
    def read_membytem(self, callback=None):
        self.table.read(6, 11, callback)
    
    def write_pcsrcm(self, value):
        self.table.write(7, 11, value)
    
    def read_pcsrcm(self, callback=None):
        self.table.read(7, 11, callback)
    
    def write_printenm(self, value):
        self.table.write(8, 11, value)
    
    def read_printenm(self, callback=None):
        self.table.read(8, 11, callback)
    
    def write_aluoutm(self, value):
        self.table.write(9, 11, value)
    
    def read_aluoutm(self, callback=None):
        self.table.read(9, 11, callback)
    
    def write_rd_specialm(self, value):
        self.table.write(10, 11, value)
    
    def read_rd_specialm(self, callback=None):
        self.table.read(10, 11, callback)
    
    def write_rdm(self, value):
        self.table.write(11, 11, value)
    
    def read_rdm(self, callback=None):
        self.table.read(11, 11, callback)
    
    def write_rd_specialm_b(self, value):
        self.table.write(12, 11, value)
    
    def read_rd_specialm_b(self, callback=None):
        self.table.read(12, 11, callback)
    
    def write_rd_specialm_c(self, value):
        self.table.write(13, 11, value)
    
    def read_rd_specialm_c(self, callback=None):
        self.table.read(13, 11, callback)
    
    def write_rd_specialm_d(self, value):
        self.table.write(14, 11, value)
    
    def read_rd_specialm_d(self, callback=None):
        self.table.read(14, 11, callback)
    
    def write_rd_specialm_e(self, value):
        self.table.write(15, 11, value)
    
    def read_rd_specialm_e(self, callback=None):
        self.table.read(15, 11, callback)
    
    def write_rd_g_a(self, value):
        self.table.write(16, 11, value)
    
    def read_rd_g_a(self, callback=None):
        self.table.read(16, 11, callback)
    
    def write_rd_d_a(self, value):
        self.table.write(17, 11, value)
    
    def read_rd_d_a(self, callback=None):
        self.table.read(17, 11, callback)
    
    def write_aluoutm_o(self, value):
        self.table.write(18, 11, value)
    
    def read_aluoutm_o(self, callback=None):
        self.table.read(18, 11, callback)
    
    #=================================================================================
    # Señales del WriteBack
    #=================================================================================
    def write_regwritesm_wb(self, value):
        self.table.write(1, 11, value)
    
    def read_regwritesm_wb(self, callback=None):
        self.table.read(1, 11, callback)
    
    def write_regwriterm_wb(self, value):
        self.table.write(2, 11, value)
    
    def read_regwriterm_wb(self, callback=None):
        self.table.read(2, 11, callback)
    
    def write_pcsrcm_wb(self, value):
        self.table.write(3, 11, value)
    
    def read_pcsrcm_wb(self, callback=None):
        self.table.read(3, 11, callback)
    
    def write_membytem_wb(self, value):
        self.table.write(4, 11, value)
    
    def read_membytem_wb(self, callback=None):
        self.table.read(4, 11, callback)
    
    def write_printenm_wb(self, value):
        self.table.write(5, 11, value)
    
    def read_printenm_wb(self, callback=None):
        self.table.read(5, 11, callback)
    
    def write_aluoutw(self, value):
        self.table.write(6, 11, value)
    
    def read_aluoutw(self, callback=None):
        self.table.read(6, 11, callback)
    
    def write_aluoutw_b(self, value):
        self.table.write(7, 11, value)
    
    def read_aluoutw_b(self, callback=None):
        self.table.read(7, 11, callback)
    
    def write_aluoutw_c(self, value):
        self.table.write(8, 11, value)
    
    def read_aluoutw_c(self, callback=None):
        self.table.read(8, 11, callback)
    
    def write_int_pl(self, value):
        self.table.write(9, 11, value)
    
    def read_int_pl(self, callback=None):
        self.table.read(9, 11, callback)
    
    def write_acii_pl(self, value):
        self.table.write(10, 11, value)
    
    def read_acii_pl(self, callback=None):
        self.table.read(10, 11, callback)
    
    def write_b_pl(self, value):
        self.table.write(11, 11, value)
    
    def read_b_pl(self, callback=None):
        self.table.read(11, 11, callback)
    
    def write_rdw(self, value):
        self.table.write(12, 11, value)
    
    def read_rdw(self, callback=None):
        self.table.read(12, 11, callback)
    
    #=================================================================================
    # Valores actuales de registros generales
    #=================================================================================
    def write_r0(self, value):
        self.table.write(1, 14, 0x00000000)
    
    def read_r0(self, callback=None):
        self.table.read(1, 14, callback)
    
    def write_r1(self, value):
        self.table.write(2, 14, value)
    
    def read_r1(self, callback=None):
        self.table.read(2, 14, callback)
    
    def write_r2(self, value):
        self.table.write(3, 14, value)
    
    def read_r2(self, callback=None):
        self.table.read(3, 14, callback)
    
    def write_r3(self, value):
        self.table.write(4, 14, value)
    
    def read_r3(self, callback=None):
        self.table.read(4, 14, callback)
    
    def write_r4(self, value):
        self.table.write(5, 14, value)
    
    def read_r4(self, callback=None):
        self.table.read(5, 14, callback)
    
    def write_r5(self, value):
        self.table.write(6, 14, value)
    
    def read_r5(self, callback=None):
        self.table.read(6, 14, callback)
    
    def write_r6(self, value):
        self.table.write(7, 14, value)
    
    def read_r6(self, callback=None):
        self.table.read(7, 14, callback)
    
    def write_r7(self, value):
        self.table.write(8, 14, value)
    
    def read_r7(self, callback=None):
        self.table.read(8, 14, callback)
    
    def write_r8(self, value):
        self.table.write(9, 14, value)
    
    def read_r8(self, callback=None):
        self.table.read(9, 14, callback)
    
    def write_r9(self, value):
        self.table.write(10, 14, value)
    
    def read_r9(self, callback=None):
        self.table.read(10, 14, callback)
    
    def write_r10(self, value):
        self.table.write(11, 14, value)
    
    def read_r10(self, callback=None):
        self.table.read(11, 14, callback)
    
    def write_r11(self, value):
        self.table.write(12, 14, value)
    
    def read_r11(self, callback=None):
        self.table.read(12, 14, callback)
    
    def write_r12(self, value):
        self.table.write(13, 14, value)
    
    def read_r12(self, callback=None):
        self.table.read(13, 14, callback)
    
    def write_r13(self, value):
        self.table.write(14, 14, value)
    
    def read_r13(self, callback=None):
        self.table.read(14, 14, callback)
    
    def write_r14(self, value):
        self.table.write(15, 14, value)
    
    def read_r14(self, callback=None):
        self.table.read(15, 14, callback)
    
    def write_r15(self, value):
        self.table.write(16, 14, value)
    
    def read_r15(self, callback=None):
        self.table.read(16, 14, callback)
    
    #=================================================================================
    # Valores actuales de registros seguros
    #=================================================================================
    def write_w1(self, value):
        self.table.write(1, 17, value)
    
    def read_w1(self, callback=None):
        self.table.read(1, 17, callback)
    
    def write_w2(self, value):
        self.table.write(2, 17, value)
    
    def read_w2(self, callback=None):
        self.table.read(2, 17, callback)
    
    def write_w3(self, value):
        self.table.write(3, 17, value)
    
    def read_w3(self, callback=None):
        self.table.read(3, 17, callback)
    
    def write_w4(self, value):
        self.table.write(4, 17, value)
    
    def read_w4(self, callback=None):
        self.table.read(4, 17, callback)
    
    def write_w5(self, value):
        self.table.write(5, 17, value)
    
    def read_w5(self, callback=None):
        self.table.read(5, 17, callback)
    
    def write_w6(self, value):
        self.table.write(6, 17, value)
    
    def read_w6(self, callback=None):
        self.table.read(6, 17, callback)
    
    def write_w7(self, value):
        self.table.write(7, 17, value)
    
    def read_w7(self, callback=None):
        self.table.read(7, 17, callback)
    
    def write_w8(self, value):
        self.table.write(8, 17, value)
    
    def read_w8(self, callback=None):
        self.table.read(8, 17, callback)
    
    def write_w9(self, value):
        self.table.write(9, 17, value)
    
    def read_w9(self, callback=None):
        self.table.read(9, 17, callback)
    
    def write_d0_safe(self, value):
        self.table.write(10, 17, value)
    
    def read_d0_safe(self, callback=None):
        self.table.read(10, 17, callback)
    
    #=================================================================================
    # Valores actuales de bloques de la contraseña
    #=================================================================================
    def write_p1(self, value):
        self.table.write(1, 20, value)
    
    def read_p1(self, callback=None):
        self.table.read(1, 20, callback)
    
    def write_p2(self, value):
        self.table.write(2, 20, value)
    
    def read_p2(self, callback=None):
        self.table.read(2, 20, callback)
    
    def write_p3(self, value):
        self.table.write(3, 20, value)
    
    def read_p3(self, callback=None):
        self.table.read(3, 20, callback)
    
    def write_p4(self, value):
        self.table.write(4, 20, value)
    
    def read_p4(self, callback=None):
        self.table.read(4, 20, callback)
    
    def write_p5(self, value):
        self.table.write(5, 20, value)
    
    def read_p5(self, callback=None):
        self.table.read(5, 20, callback)
    
    def write_p6(self, value):
        self.table.write(6, 20, value)
    
    def read_p6(self, callback=None):
        self.table.read(6, 20, callback)
    
    def write_p7(self, value):
        self.table.write(7, 20, value)
    
    def read_p7(self, callback=None):
        self.table.read(7, 20, callback)
    
    def write_p8(self, value):
        self.table.write(8, 20, value)
    
    def read_p8(self, callback=None):
        self.table.read(8, 20, callback)
    
    #=================================================================================
    # Valores actuales de registros generales k
    #=================================================================================
    def write_k0_0(self, value):
        self.table.write(1, 23, value)
    
    def read_k0_0(self, callback=None):
        self.table.read(1, 23, callback)
    
    def write_k0_1(self, value):
        self.table.write(2, 23, value)
    
    def read_k0_1(self, callback=None):
        self.table.read(2, 23, callback)
    
    def write_k0_2(self, value):
        self.table.write(3, 23, value)
    
    def read_k0_2(self, callback=None):
        self.table.read(3, 23, callback)
    
    def write_k0_3(self, value):
        self.table.write(4, 23, value)
    
    def read_k0_3(self, callback=None):
        self.table.read(4, 23, callback)
    
    def write_k1_0(self, value):
        self.table.write(5, 23, value)
    
    def read_k1_0(self, callback=None):
        self.table.read(5, 23, callback)
    
    def write_k1_1(self, value):
        self.table.write(6, 23, value)
    
    def read_k1_1(self, callback=None):
        self.table.read(6, 23, callback)
    
    def write_k1_2(self, value):
        self.table.write(7, 23, value)
    
    def read_k1_2(self, callback=None):
        self.table.read(7, 23, callback)
    
    def write_k1_3(self, value):
        self.table.write(8, 23, value)
    
    def read_k1_3(self, callback=None):
        self.table.read(8, 23, callback)
    
    def write_k2_0(self, value):
        self.table.write(9, 23, value)
    
    def read_k2_0(self, callback=None):
        self.table.read(9, 23, callback)
    
    def write_k2_1(self, value):
        self.table.write(10, 23, value)
    
    def read_k2_1(self, callback=None):
        self.table.read(10, 23, callback)
    
    def write_k2_2(self, value):
        self.table.write(11, 23, value)
    
    def read_k2_2(self, callback=None):
        self.table.read(11, 23, callback)
    
    def write_k2_3(self, value):
        self.table.write(12, 23, value)
    
    def read_k2_3(self, callback=None):
        self.table.read(12, 23, callback)
    
    def write_k3_0(self, value):
        self.table.write(13, 23, value)
    
    def read_k3_0(self, callback=None):
        self.table.read(13, 23, callback)
    
    def write_k3_1(self, value):
        self.table.write(14, 23, value)
    
    def read_k3_1(self, callback=None):
        self.table.read(14, 23, callback)
    
    def write_k3_2(self, value):
        self.table.write(15, 23, value)
    
    def read_k3_2(self, callback=None):
        self.table.read(15, 23, callback)
    
    def write_k3_3(self, value):
        self.table.write(16, 23, value)
    
    def read_k3_3(self, callback=None):
        self.table.read(16, 23, callback)
    
    #=================================================================================
    # Valores actuales de la memoria general
    #=================================================================================
    def write_g0(self, value):
        self.table.write(1, 26, value)
    
    def read_g0(self, callback=None):
        self.table.read(1, 26, callback)
    
    def write_g1(self, value):
        self.table.write(2, 26, value)
    
    def read_g1(self, callback=None):
        self.table.read(2, 26, callback)
    
    def write_g2(self, value):
        self.table.write(3, 26, value)
    
    def read_g2(self, callback=None):
        self.table.read(3, 26, callback)
    
    def write_g3(self, value):
        self.table.write(4, 26, value)
    
    def read_g3(self, callback=None):
        self.table.read(4, 26, callback)
    
    def write_g4(self, value):
        self.table.write(5, 26, value)
    
    def read_g4(self, callback=None):
        self.table.read(5, 26, callback)
    
    def write_g5(self, value):
        self.table.write(6, 26, value)
    
    def read_g5(self, callback=None):
        self.table.read(6, 26, callback)
    
    def write_g6(self, value):
        self.table.write(7, 26, value)
    
    def read_g6(self, callback=None):
        self.table.read(7, 26, callback)
    
    def write_g7(self, value):
        self.table.write(8, 26, value)
    
    def read_g7(self, callback=None):
        self.table.read(8, 26, callback)
    
    def write_g8(self, value):
        self.table.write(9, 26, value)
    
    def read_g8(self, callback=None):
        self.table.read(9, 26, callback)
    
    def write_g9(self, value):
        self.table.write(10, 26, value)
    
    def read_g9(self, callback=None):
        self.table.read(10, 26, callback)
    
    def write_g10(self, value):
        self.table.write(11, 26, value)
    
    def read_g10(self, callback=None):
        self.table.read(11, 26, callback)
    
    def write_g11(self, value):
        self.table.write(12, 26, value)
    
    def read_g11(self, callback=None):
        self.table.read(12, 26, callback)
    
    def write_g12(self, value):
        self.table.write(13, 26, value)
    
    def read_g12(self, callback=None):
        self.table.read(13, 26, callback)
    
    def write_g13(self, value):
        self.table.write(14, 26, value)
    
    def read_g13(self, callback=None):
        self.table.read(14, 26, callback)
    
    def write_g14(self, value):
        self.table.write(15, 26, value)
    
    def read_g14(self, callback=None):
        self.table.read(15, 26, callback)
    
    def write_g15(self, value):
        self.table.write(16, 26, value)
    
    def read_g15(self, callback=None):
        self.table.read(16, 26, callback)
    
    def write_g16(self, value):
        self.table.write(17, 26, value)
    
    def read_g16(self, callback=None):
        self.table.read(17, 26, callback)
    
    def write_g17(self, value):
        self.table.write(18, 26, value)
    
    def read_g17(self, callback=None):
        self.table.read(18, 26, callback)
    
    def write_g18(self, value):
        self.table.write(19, 26, value)
    
    def read_g18(self, callback=None):
        self.table.read(19, 26, callback)
    
    def write_g19(self, value):
        self.table.write(20, 26, value)
    
    def read_g19(self, callback=None):
        self.table.read(20, 26, callback)
    
    def write_g20(self, value):
        self.table.write(21, 26, value)
    
    def read_g20(self, callback=None):
        self.table.read(21, 26, callback)
    
    def write_g21(self, value):
        self.table.write(22, 26, value)
    
    def read_g21(self, callback=None):
        self.table.read(22, 26, callback)
    
    def write_g22(self, value):
        self.table.write(23, 26, value)
    
    def read_g22(self, callback=None):
        self.table.read(23, 26, callback)
    
    def write_g23(self, value):
        self.table.write(24, 26, value)
    
    def read_g23(self, callback=None):
        self.table.read(24, 26, callback)
    
    def write_g24(self, value):
        self.table.write(25, 26, value)
    
    def read_g24(self, callback=None):
        self.table.read(25, 26, callback)
    
    def write_g25(self, value):
        self.table.write(26, 26, value)
    
    def read_g25(self, callback=None):
        self.table.read(26, 26, callback)
    
    def write_g26(self, value):
        self.table.write(27, 26, value)
    
    def read_g26(self, callback=None):
        self.table.read(27, 26, callback)
    
    def write_g27(self, value):
        self.table.write(28, 26, value)
    
    def read_g27(self, callback=None):
        self.table.read(28, 26, callback)
    
    def write_g28(self, value):
        self.table.write(29, 26, value)
    
    def read_g28(self, callback=None):
        self.table.read(29, 26, callback)
    
    def write_g29(self, value):
        self.table.write(30, 26, value)
    
    def read_g29(self, callback=None):
        self.table.read(30, 26, callback)
    
    def write_g30(self, value):
        self.table.write(31, 26, value)
    
    def read_g30(self, callback=None):
        self.table.read(31, 26, callback)
    
    def write_g31(self, value):
        self.table.write(32, 26, value)
    
    def read_g31(self, callback=None):
        self.table.read(32, 26, callback)
    
    def write_g32(self, value):
        self.table.write(33, 26, value)
    
    def read_g32(self, callback=None):
        self.table.read(33, 26, callback)
    
    def write_g33(self, value):
        self.table.write(34, 26, value)
    
    def read_g33(self, callback=None):
        self.table.read(34, 26, callback)
    
    def write_g34(self, value):
        self.table.write(35, 26, value)
    
    def read_g34(self, callback=None):
        self.table.read(35, 26, callback)
    
    def write_g35(self, value):
        self.table.write(36, 26, value)
    
    def read_g35(self, callback=None):
        self.table.read(36, 26, callback)
    
    def write_g36(self, value):
        self.table.write(37, 26, value)
    
    def read_g36(self, callback=None):
        self.table.read(37, 26, callback)
    
    def write_g37(self, value):
        self.table.write(38, 26, value)
    
    def read_g37(self, callback=None):
        self.table.read(38, 26, callback)
    
    def write_g38(self, value):
        self.table.write(39, 26, value)
    
    def read_g38(self, callback=None):
        self.table.read(39, 26, callback)
    
    def write_g39(self, value):
        self.table.write(40, 26, value)
    
    def read_g39(self, callback=None):
        self.table.read(40, 26, callback)
    
    def write_g40(self, value):
        self.table.write(41, 26, value)
    
    def read_g40(self, callback=None):
        self.table.read(41, 26, callback)
    
    def write_g41(self, value):
        self.table.write(42, 26, value)
    
    def read_g41(self, callback=None):
        self.table.read(42, 26, callback)
    
    def write_g42(self, value):
        self.table.write(43, 26, value)
    
    def read_g42(self, callback=None):
        self.table.read(43, 26, callback)
    
    def write_g43(self, value):
        self.table.write(44, 26, value)
    
    def read_g43(self, callback=None):
        self.table.read(44, 26, callback)
    
    def write_g44(self, value):
        self.table.write(45, 26, value)
    
    def read_g44(self, callback=None):
        self.table.read(45, 26, callback)
    
    def write_g45(self, value):
        self.table.write(46, 26, value)
    
    def read_g45(self, callback=None):
        self.table.read(46, 26, callback)
    
    def write_g46(self, value):
        self.table.write(47, 26, value)
    
    def read_g46(self, callback=None):
        self.table.read(47, 26, callback)
    
    def write_g47(self, value):
        self.table.write(48, 26, value)
    
    def read_g47(self, callback=None):
        self.table.read(48, 26, callback)
    
    def write_g48(self, value):
        self.table.write(49, 26, value)
    
    def read_g48(self, callback=None):
        self.table.read(49, 26, callback)
    
    def write_g49(self, value):
        self.table.write(50, 26, value)
    
    def read_g49(self, callback=None):
        self.table.read(50, 26, callback)
    
    def write_g50(self, value):
        self.table.write(51, 26, value)
    
    def read_g50(self, callback=None):
        self.table.read(51, 26, callback)
    
    def write_g51(self, value):
        self.table.write(52, 26, value)
    
    def read_g51(self, callback=None):
        self.table.read(52, 26, callback)
    
    def write_g52(self, value):
        self.table.write(53, 26, value)
    
    def read_g52(self, callback=None):
        self.table.read(53, 26, callback)
    
    def write_g53(self, value):
        self.table.write(54, 26, value)
    
    def read_g53(self, callback=None):
        self.table.read(54, 26, callback)
    
    def write_g54(self, value):
        self.table.write(55, 26, value)
    
    def read_g54(self, callback=None):
        self.table.read(55, 26, callback)
    
    def write_g55(self, value):
        self.table.write(56, 26, value)
    
    def read_g55(self, callback=None):
        self.table.read(56, 26, callback)
    
    def write_g56(self, value):
        self.table.write(57, 26, value)
    
    def read_g56(self, callback=None):
        self.table.read(57, 26, callback)
    
    def write_g57(self, value):
        self.table.write(58, 26, value)
    
    def read_g57(self, callback=None):
        self.table.read(58, 26, callback)
    
    def write_g58(self, value):
        self.table.write(59, 26, value)
    
    def read_g58(self, callback=None):
        self.table.read(59, 26, callback)
    
    def write_g59(self, value):
        self.table.write(60, 26, value)
    
    def read_g59(self, callback=None):
        self.table.read(60, 26, callback)
    
    def write_g60(self, value):
        self.table.write(61, 26, value)
    
    def read_g60(self, callback=None):
        self.table.read(61, 26, callback)
    
    def write_g61(self, value):
        self.table.write(62, 26, value)
    
    def read_g61(self, callback=None):
        self.table.read(62, 26, callback)
    
    def write_g62(self, value):
        self.table.write(63, 26, value)
    
    def read_g62(self, callback=None):
        self.table.read(63, 26, callback)
    
    def write_g63(self, value):
        self.table.write(64, 26, value)
    
    def read_g63(self, callback=None):
        self.table.read(64, 26, callback)
    
    #=================================================================================
    # Valores actuales de la memoria dinámica (posición inicial)
    #=================================================================================
    def write_d0(self, value):
        self.table.write(1, 29, value)
    
    def read_d0(self, callback=None):
        self.table.read(1, 29, callback)
        
    #=================================================================================
    # Funcion de reset para el inicio del simulador
    #=================================================================================
    def reset(self):
        """Resetea todas las señales a sus valores iniciales y escribe sus nombres"""
        # Señales del Decode
        self.table.write(1, 1, "PC'")
        self.table.write(1, 2, "0x00000000")
        self.table.write(2, 1, "PCF")
        self.table.write(2, 2, "0x00000000")
        self.table.write(3, 1, "PCPlus8F")
        self.table.write(3, 2, "0x00001000")
        self.table.write(4, 1, "InstrF")
        self.table.write(4, 2, "0x300000000000000")
        
        # Señales del Fetch
        self.table.write(1, 4, "InstrD")
        self.table.write(1, 5, "0x300000000000000")
        self.table.write(2, 4, "PCF_D")
        self.table.write(2, 5, "0x00000000")
        self.table.write(3, 4, "55:52")
        self.table.write(3, 5, "0b0000")
        self.table.write(4, 4, "63:56")
        self.table.write(4, 5, "0b00110000")
        self.table.write(5, 4, "47:44")
        self.table.write(5, 5, "0b0000")
        self.table.write(6, 4, "43:40")
        self.table.write(6, 5, "0b0000")
        self.table.write(7, 4, "39:8")
        self.table.write(7, 5, "0x00000000")
        self.table.write(8, 4, "51:48")
        self.table.write(8, 5, "0b0000")
        self.table.write(9, 4, "MemWriteP")
        self.table.write(9, 5, "0b0")
        self.table.write(10, 4, "MemWriteV")
        self.table.write(10, 5, "0b0")
        self.table.write(11, 4, "RegisterInA")
        self.table.write(11, 5, "0b1")
        self.table.write(12, 4, "RegisterInB")
        self.table.write(12, 5, "0b00")
        self.table.write(13, 4, "ImmediateOp")
        self.table.write(13, 5, "0b0")
        self.table.write(14, 4, "BranchE")
        self.table.write(14, 5, "0b0")
        self.table.write(15, 4, "LogOutD")
        self.table.write(15, 5, "0b0")
        self.table.write(16, 4, "ComSD")
        self.table.write(16, 5, "0b0")
        self.table.write(17, 4, "PrintEnD")
        self.table.write(17, 5, "0b11")
        self.table.write(18, 4, "RegWriteSD")
        self.table.write(18, 5, "0b0")
        self.table.write(19, 4, "RegWriteRD")
        self.table.write(19, 5, "0b0")
        self.table.write(21, 4, "MemOpD")
        self.table.write(21, 5, "0b11")
        self.table.write(22, 4, "MemWriteGD")
        self.table.write(22, 5, "0b0")
        self.table.write(23, 4, "MemWriteDD")
        self.table.write(23, 5, "0b0")
        self.table.write(24, 4, "MemByteD")
        self.table.write(24, 5, "0b0")
        self.table.write(25, 4, "PCSrcD")
        self.table.write(25, 5, "0b0")
        self.table.write(26, 4, "FlagsUpdD")
        self.table.write(26, 5, "0b0")
        self.table.write(27, 4, "ALUSrcD")
        self.table.write(27, 5, "0b000000")
        self.table.write(28, 4, "BranchOpD")
        self.table.write(28, 5, "0b111")
        self.table.write(29, 4, "RDr1_a")
        self.table.write(29, 5, "0x00000000")
        self.table.write(30, 4, "RDr2_a")
        self.table.write(30, 5, "0x00000000")
        self.table.write(31, 4, "RDw1_a")
        self.table.write(31, 5, "0x00000000")
        self.table.write(32, 4, "RDw2_a")
        self.table.write(32, 5, "0x00000000")
        self.table.write(33, 4, "KD_a")
        self.table.write(33, 5, "0x00000000")
        self.table.write(34, 4, "RD_a")
        self.table.write(34, 5, "0x00000000")
        self.table.write(35, 4, "SrcAD_0")
        self.table.write(35, 5, "0x00000000")
        self.table.write(36, 4, "SrcAD")
        self.table.write(36, 5, "0x00000000")
        self.table.write(37, 4, "Rd_SpecialD")
        self.table.write(37, 5, "0x00000000")
        self.table.write(38, 4, "SrcBD")
        self.table.write(38, 5, "0x00000000")
        
        # Señales del Execute
        self.table.write(1, 7, "RegWriteSE")
        self.table.write(1, 8, "0b0")
        self.table.write(2, 7, "RegWriteRE")
        self.table.write(2, 8, "0b0")
        self.table.write(3, 7, "MemOpE")
        self.table.write(3, 8, "0b11")
        self.table.write(4, 7, "MemWriteGE")
        self.table.write(4, 8, "0b0")
        self.table.write(5, 7, "MemWriteDE")
        self.table.write(5, 8, "0b0")
        self.table.write(6, 7, "MemByteE")
        self.table.write(6, 8, "0b0")
        self.table.write(7, 7, "PCSrcE")
        self.table.write(7, 8, "0b0")
        self.table.write(8, 7, "FlagsUpdE")
        self.table.write(8, 8, "0b0")
        self.table.write(9, 7, "ALUSrcE")
        self.table.write(9, 8, "0b000000")
        self.table.write(10, 7, "BranchOpE")
        self.table.write(10, 8, "0b111")
        self.table.write(11, 7, "PrintEnE")
        self.table.write(11, 8, "0b11")
        self.table.write(12, 7, "ComSE")
        self.table.write(12, 8, "0b0")
        self.table.write(13, 7, "LogOutE")
        self.table.write(13, 8, "0b0")
        self.table.write(14, 7, "BranchOpE")
        self.table.write(14, 8, "0b111")
        self.table.write(15, 7, "FlagsE")
        self.table.write(15, 8, "0b0000")
        self.table.write(16, 7, "SrcAE")
        self.table.write(16, 8, "0x00000000")
        self.table.write(17, 7, "RD_SpecialE")
        self.table.write(17, 8, "0x00000000")
        self.table.write(18, 7, "SrcBE")
        self.table.write(18, 8, "0x00000000")
        self.table.write(19, 7, "Flags'")
        self.table.write(19, 8, "0b0000")
        self.table.write(20, 7, "ALUFlagOut")
        self.table.write(20, 8, "0b0000")
        self.table.write(21, 7, "CarryIn")
        self.table.write(21, 8, "0b0")
        self.table.write(22, 7, "CondExE")
        self.table.write(22, 8, "0b0")
        self.table.write(23, 7, "SafeFlagsOut")
        self.table.write(23, 8, "0b00")
        self.table.write(24, 7, "LoginInBlockE")
        self.table.write(24, 8, "0b0000")
        self.table.write(25, 7, "RdE")
        self.table.write(25, 8, "0b0000")
        self.table.write(26, 7, "ALUResultE")
        self.table.write(26, 8, "0x00000000")
        self.table.write(27, 7, "PCSrc_AND_E")
        self.table.write(27, 8, "0b0")
        
        # Señales del Memory
        self.table.write(1, 10, "RegWriteSM")
        self.table.write(1, 11, "0b0")
        self.table.write(2, 10, "RegWriteRM")
        self.table.write(2, 11, "0b0")
        self.table.write(3, 10, "MemOpM")
        self.table.write(3, 11, "0b11")
        self.table.write(4, 10, "MemWriteGM")
        self.table.write(4, 11, "0b0")
        self.table.write(5, 10, "MemWriteDM")
        self.table.write(5, 11, "0b0")
        self.table.write(6, 10, "MemByteM")
        self.table.write(6, 11, "0b0")
        self.table.write(7, 10, "PCSrcM")
        self.table.write(7, 11, "0b0")
        self.table.write(8, 10, "PrintEnM")
        self.table.write(8, 11, "0b11")
        self.table.write(9, 10, "ALUOutM")
        self.table.write(9, 11, "0x00000000")
        self.table.write(10, 10, "RD_SpecialM")
        self.table.write(10, 11, "0x00000000")
        self.table.write(11, 10, "RdM")
        self.table.write(11, 11, "0b0000")
        self.table.write(12, 10, "RD_SpecialM_b")
        self.table.write(12, 11, "0x00000000")
        self.table.write(13, 10, "RD_SpecialM_c")
        self.table.write(13, 11, "0x00000000")
        self.table.write(14, 10, "RD_SpecialM_d")
        self.table.write(14, 11, "0x00000000")
        self.table.write(15, 10, "RD_SpecialM_e")
        self.table.write(15, 11, "0x00000000")
        self.table.write(16, 10, "RD_G_a")
        self.table.write(16, 11, "0x00000000")
        self.table.write(17, 10, "RD_D_a")
        self.table.write(17, 11, "0x00000000")
        self.table.write(18, 10, "ALUOutM_O")
        self.table.write(18, 11, "0x00000000")
        
        # Señales del WriteBack
        self.table.write(1, 10, "RegWriteSM")
        self.table.write(1, 11, "0b0")
        self.table.write(2, 10, "RegWriteRM")
        self.table.write(2, 11, "0b0")
        self.table.write(3, 10, "PCSrcM")
        self.table.write(3, 11, "0b0")
        self.table.write(4, 10, "MemByteM")
        self.table.write(4, 11, "0b0")
        self.table.write(5, 10, "PrintEnM")
        self.table.write(5, 11, "0b11")
        self.table.write(6, 10, "ALUOutW")
        self.table.write(6, 11, "0x00000000")
        self.table.write(7, 10, "ALUOutW_b")
        self.table.write(7, 11, "0x00000000")
        self.table.write(8, 10, "ALUOutW_c")
        self.table.write(8, 11, "0x00000000")
        self.table.write(9, 10, "int_pl")
        self.table.write(9, 11, "0x00000000")
        self.table.write(10, 10, "ACII_pl")
        self.table.write(10, 11, "0x00000000")
        self.table.write(11, 10, "b_pl")
        self.table.write(11, 11, "0x00000000")
        self.table.write(12, 10, "RdW")
        self.table.write(12, 11, "0b0000")
        
        # Valores actuales de registros generales
        self.table.write(1, 13, "R0")
        self.table.write(1, 14, "0x00000000")
        self.table.write(2, 13, "R1")
        self.table.write(2, 14, "0x00000000")
        self.table.write(3, 13, "R2")
        self.table.write(3, 14, "0x00000000")
        self.table.write(4, 13, "R3")
        self.table.write(4, 14, "0x00000000")
        self.table.write(5, 13, "R4")
        self.table.write(5, 14, "0x00000000")
        self.table.write(6, 13, "R5")
        self.table.write(6, 14, "0x00000000")
        self.table.write(7, 13, "R6")
        self.table.write(7, 14, "0x00000000")
        self.table.write(8, 13, "R7")
        self.table.write(8, 14, "0x00000000")
        self.table.write(9, 13, "R8")
        self.table.write(9, 14, "0x00000000")
        self.table.write(10, 13, "R9")
        self.table.write(10, 14, "0x00000000")
        self.table.write(11, 13, "R10")
        self.table.write(11, 14, "0x00000000")
        self.table.write(12, 13, "R11")
        self.table.write(12, 14, "0x00000000")
        self.table.write(13, 13, "R12")
        self.table.write(13, 14, "0x00000000")
        self.table.write(14, 13, "R13")
        self.table.write(14, 14, "0x00000000")
        self.table.write(15, 13, "R14")
        self.table.write(15, 14, "0x00000000")
        self.table.write(16, 13, "R15")
        self.table.write(16, 14, "0x00000000")
        
        # Valores actuales de registros seguros
        self.table.write(1, 16, "W1")
        self.table.write(1, 17, "0x00000000")
        self.table.write(2, 16, "W2")
        self.table.write(2, 17, "0x00000000")
        self.table.write(3, 16, "W3")
        self.table.write(3, 17, "0x00000000")
        self.table.write(4, 16, "W4")
        self.table.write(4, 17, "0x00000000")
        self.table.write(5, 16, "W5")
        self.table.write(5, 17, "0x00000000")
        self.table.write(6, 16, "W6")
        self.table.write(6, 17, "0x00000000")
        self.table.write(7, 16, "W7")
        self.table.write(7, 17, "0x00000000")
        self.table.write(8, 16, "W8")
        self.table.write(8, 17, "0x00000000")
        self.table.write(9, 16, "W9")
        self.table.write(9, 17, "0x00000000")
        self.table.write(10, 16, "D0")
        self.table.write(10, 17, "0x9E3779B9")
        
        # Valores actuales de bloques de la contraseña
        self.table.write(1, 19, "P1")
        self.table.write(1, 20, "0x00000001")
        self.table.write(2, 19, "P2")
        self.table.write(2, 20, "0x00000010")
        self.table.write(3, 19, "P3")
        self.table.write(3, 20, "0x00000011")
        self.table.write(4, 19, "P4")
        self.table.write(4, 20, "0x00000100")
        self.table.write(5, 19, "P5")
        self.table.write(5, 20, "0x00000101")
        self.table.write(6, 19, "P6")
        self.table.write(6, 20, "0x00000110")
        self.table.write(7, 19, "P7")
        self.table.write(7, 20, "0x00000111")
        self.table.write(8, 19, "P8")
        self.table.write(8, 20, "0x00001000")
        
        # Valores actuales de registros generales k
        self.table.write(1, 22, "k0.0")
        self.table.write(1, 23, "0x00000000")
        self.table.write(2, 22, "k0.1")
        self.table.write(2, 23, "0x00000000")
        self.table.write(3, 22, "k0.2")
        self.table.write(3, 23, "0x00000000")
        self.table.write(4, 22, "k0.3")
        self.table.write(4, 23, "0x00000000")
        self.table.write(5, 22, "k1.0")
        self.table.write(5, 23, "0x00000000")
        self.table.write(6, 22, "k1.1")
        self.table.write(6, 23, "0x00000000")
        self.table.write(7, 22, "k1.2")
        self.table.write(7, 23, "0x00000000")
        self.table.write(8, 22, "k1.3")
        self.table.write(8, 23, "0x00000000")
        self.table.write(9, 22, "k2.0")
        self.table.write(9, 23, "0x00000000")
        self.table.write(10, 22, "k2.1")
        self.table.write(10, 23, "0x00000000")
        self.table.write(11, 22, "k2.2")
        self.table.write(11, 23, "0x00000000")
        self.table.write(12, 22, "k2.3")
        self.table.write(12, 23, "0x00000000")
        self.table.write(13, 22, "k3.0")
        self.table.write(13, 23, "0x00000000")
        self.table.write(14, 22, "k3.1")
        self.table.write(14, 23, "0x00000000")
        self.table.write(15, 22, "k3.2")
        self.table.write(15, 23, "0x00000000")
        self.table.write(16, 22, "k3.3")
        self.table.write(16, 23, "0x00000000")
        
        self.table.execute_all()