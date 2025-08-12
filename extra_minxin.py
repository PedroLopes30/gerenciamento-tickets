#imports
from abc import abstractmethod,ABC
from os import remove

#interfaces

class IArquivo(
    ABC
):
    @abstractmethod
    def ler_arquivo(self)->str:
        pass
    
    @abstractmethod
    def escrever_arquivo(self,conteudo)->None:
        pass
    
  
#minxins  
class Manipular_arquivo(
    IArquivo
):
    def __init__(self,arquivo):
        self.arquivo = arquivo
        
    def ler_arquivo(self,raise_erro=True):
        try:
            with open(self.arquivo,'r') as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            if raise_erro:
                print("Arquivo não encontrado, não é possivel realizar o relatorio")
            
        except Exception as e:
            print("Erro desconhecido : ",e)
            
    
    def escrever_arquivo(self,conteudo):
        try: 
           with open(self.arquivo,'w') as file:
               file.write(conteudo)
               
        except Exception as e:
            print("Erro desconhecido : ",e)
            

class Relatorio(
    Manipular_arquivo
):
    def __init__(self, arquivo):
        super().__init__(arquivo)
        
    def adicionar_linha(self,linha)->bool:
        conteudo_existente = self.ler_arquivo()
        if not conteudo_existente:
            self.escrever_arquivo(f"{linha} \n")
            return True
        
        novo_conteudo = f"{conteudo_existente + linha} \n"
        self.escrever_arquivo(novo_conteudo)
        return True
    
    def rescrever_arquivo(self,conteudo):
        conteudo_existente = self.ler_arquivo(raise_erro=False)
        if not conteudo_existente:
            self.escrever_arquivo(conteudo)
            return True
        
        novo_conteudo = conteudo_existente + conteudo
        self.escrever_arquivo(novo_conteudo)
        return True
        
        
#func
def excluir_arquivo(caminho)->None:
    try:
        remove(caminho)
        print(f"✅ Arquivo removido: {caminho}")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
    except PermissionError:
        print(f"Permissão negada para excluir: {caminho}")
    except Exception as e:
        print(f"Erro ao excluir o arquivo: {e}")
