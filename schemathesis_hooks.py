import schemathesis

@schemathesis.check
def custom_security_header_check(ctx, response, case):
    """
    ÖZEL GÜVENLİK KURALI:
    Herhangi bir API isteğinde, dönen cevabın 'X-Security-Protection' isminde
    bir HTTP başlığına (header) sahip olup olmadığını denetler.
    Şirket içi güvenlik standartlarını zorunlu kılmak için harika bir örnektir.
    """
    headers = {k.lower(): v for k, v in response.headers.items()}
    if "x-security-protection" not in headers:
        raise AssertionError("Güvenlik İhlali: 'X-Security-Protection' başlığı eksik! (Security Policy Violation)")
