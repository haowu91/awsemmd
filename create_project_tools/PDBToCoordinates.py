#!/shared/local/bin/python

import sys
from VectorAlgebra import *

an = 0.4831806
bn = 0.7032820
cn = -0.1864262
ap = 0.4436538
bp = 0.2352006
cp = 0.3211455

aH = -0.946747
bH = 2.50352
cH = -0.620388

atom_type = {'1' : 'C', '2' : 'N', '3' : 'O', '4' : 'C', '5' : 'H', '6' : 'C'}
atom_desc = {'1' : 'C-Alpha', '2' : 'N', '3' : 'O', '4' : 'C-Beta', '5' : 'H-Beta', '6' : 'C-Prime'}
PDB_type = {'1' : 'CA', '2' : 'N', '3' : 'O', '4' : 'CB', '5' : 'HB', '6' : 'C' }

class Atom:
    ty = ''
    x = 0.0
    y = 0.0
    z = 0.0
    
    def __init__(self, No, ty, x, y, z, desc=''):
        self.No = No
        self.ty = ty
        self.x = x
        self.y = y
        self.z = z
        self.desc = desc

    def print_(self):
        print self.No, self.ty , self.x, ',', self.y, ',', self.z, self.desc

    def write_(self, f):
        f.write(str(self.No))
        f.write('\t')
        f.write(self.ty)
        f.write('  ')
        f.write( ("               "+str(round(self.x,8)))[-15:] )
        f.write('\t')
        f.write( ("               "+str(round(self.y,8)))[-15:] )
        f.write('\t')
        f.write( ("               "+str(round(self.z,8)))[-15:] )
        if self.desc!='':
            f.write('\t\t')
            f.write( self.desc )
        f.write('\n')

def print_array(a):
    for ia in a:
        print ia

class PDB_Atom:
	no = 0
	ty = ''
	res = 'UNK'
	res_no = 0
	x = 0.0
	y = 0.0
	z = 0.0
	atm = 'C'
	
	def __init__(self, no, ty, res, res_no, x, y, z, atm):
		self.no = no
		self.ty = ty
		self.res = res
		self.res_no = res_no
		self.x = x
		self.y = y
		self.z = z
		self.atm = atm
		
	def write_(self, f):
		f.write('ATOM')
		f.write(('       '+str(self.no))[-7:])
		f.write('  ')
		f.write((self.ty+'    ')[:4])
		f.write(self.res)
		f.write(' ')
		f.write('T')
		f.write(('    '+str(self.res_no))[-4:])
		f.write(('            '+str(round(self.x,3)))[-12:])
		f.write(('        '+str(round(self.y,3)))[-8:])
		f.write(('        '+str(round(self.z,3)))[-8:])
		f.write('  1.00')
		f.write('  0.00')
		f.write(('            '+self.atm)[-12:]+'  ')
		f.write('\n')
	
	def print_(self):
		pass

def three2one(prot):
    """ translate a protein sequence from 3 to 1 letter code"""
    
    code = {"GLY" : "G", "ALA" : "A", "LEU" : "L", "ILE" : "I",
            "ARG" : "R", "LYS" : "K", "MET" : "M", "CYS" : "C",
            "TYR" : "Y", "THR" : "T", "PRO" : "P", "SER" : "S",
            "TRP" : "W", "ASP" : "D", "GLU" : "E", "ASN" : "N",
	    "GLN" : "Q", "PHE" : "F", "HIS" : "H", "VAL" : "V"}
    
    newprot = ""
    for a in prot:
        newprot += code.get(a, "?")
    
    return newprot

if len(sys.argv)==1:
    print "\nReadingPDBFile.py PDB_Id Output_file [-s]\n"
    print "-s\tSplit into files for each chain"
#    sys.argv.append("1BG8")
    exit()

from Bio.PDB.PDBParser import PDBParser

p = PDBParser(PERMISSIVE=1)

struct_id = sys.argv[1]
filename = struct_id + ".pdb"

splite = False
for av in sys.argv:
    if av=="-s":
        splite = True
        sys.argv.remove(av)
        break

output_fn = ""
if len(sys.argv)>2: output_fn = sys.argv[2]
if output_fn[-4:]==".pdb": output_fn = output_fn[:-4]

if output_fn!="" and not splite:
    out = open( (output_fn), 'w' )

s = p.get_structure(struct_id, filename)
chains = s[0].get_list()
for ch in chains:
    sequance = []
    atoms = []
    ires = 0
    iatom = 0
    if output_fn!="":
	pass
#        if not splite:
#            out.write("Chain: ")
#            out.write(ch.get_id())
#            out.write('\n')
    else:
        print "Chain:", ch.get_id()
    for res in ch:
        is_regular_res = res.has_id('N') and res.has_id('CA') and res.has_id('C')
        if res.get_id()[0]==' ' and is_regular_res:
            ires = ires + 1
            if res:
                sequance.append(res.get_resname())
            xyz_N = res['N'].get_coord()
            xyz_CA = res['CA'].get_coord()
            xyz_C = res['C'].get_coord()
            xyz_O = res['O'].get_coord()
            if res.has_id('CB'):
                xyz_CB = res['CB'].get_coord()
            else:
                xyz_H = [0.0, 0.0, 0.0]
                xyz_H[0] = aH*xyz_N[0] + bH*xyz_CA[0] + cH*xyz_C[0]
                xyz_H[1] = aH*xyz_N[1] + bH*xyz_CA[1] + cH*xyz_C[1]
                xyz_H[2] = aH*xyz_N[2] + bH*xyz_CA[2] + cH*xyz_C[2]
            
            iatom = iatom + 1
            atom = Atom(iatom, 'N', xyz_N[0], xyz_N[1], xyz_N[2], 'N')
            atoms.append(atom)
            
            iatom = iatom + 1
            atom = Atom(iatom, 'C', xyz_CA[0], xyz_CA[1], xyz_CA[2], 'C-Alpha')
            atoms.append(atom)
            
            iatom = iatom + 1
            atom = Atom(iatom, 'C', xyz_C[0], xyz_C[1], xyz_C[2], 'C-Prime')
            atoms.append(atom)
            
            iatom = iatom + 1
            atom = Atom(iatom, 'O', xyz_O[0], xyz_O[1], xyz_O[2], 'O')
            atoms.append(atom)
            
            if res.has_id('CB'):
                iatom = iatom + 1
                atom = Atom(iatom, 'C', xyz_CB[0], xyz_CB[1], xyz_CB[2], 'C-Beta')
                atoms.append(atom)
            else:            
                iatom = iatom + 1
                atom = Atom(iatom, 'H', xyz_N[0], xyz_H[1], xyz_H[2], 'H-Beta')
                atoms.append(atom)
            
    if output_fn!="":
        if splite and len(sequance)==0: continue
        if splite:
            if len(chains)==1:
                file_name = output_fn
            else:
                file_name = output_fn+"_"+ch.get_id()
            out = open( file_name, 'w' )
        for iAtm in atoms:
            iAtm.write_(out)
        if splite:
            out.write('\n')
        if splite:
            out.close()
    else:
        print three2one(sequance)
        for iAtm in atoms:
            iAtm.print_()

if output_fn!="" and not splite:
    out.close()