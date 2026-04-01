from django.db import models

class Comentario(models.Model):
    # Relaciona o comentário ao ID do notebook que vem da API do Mercado Livre
    notebook_id = models.CharField(max_length=100)
    usuario_nome = models.CharField(max_length=100, default="Anônimo")
    texto = models.TextField()
    estrelas = models.IntegerField(default=5)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario_nome} - {self.notebook_id}"